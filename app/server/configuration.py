import os
import server.constants as constants
from loguru import logger
from dynaconf import Dynaconf, Validator
from collections import namedtuple
from server.utils.validation import validate_file_exists
from server.exceptions.validation_exception import ValidationException

# Directory paths
root_dir = os.path.abspath(os.curdir)
config_dir = os.path.join(root_dir, "config")
if os.path.exists(config_dir) is False:
    raise ValidationException(f"Config directory required at {config_dir}")

# Host env variables
for key, value in os.environ.items():
    logger.debug(f"OS ENV: {key}={value}")

# Setting file name constants
FileNameConstants = namedtuple(
    "FileNameConstants",
    ["file_name_settings", "file_name_settings_local", "file_name_secrets_local"],
)
file_name_constants = FileNameConstants(
    "settings.toml",  # defaults - committed to git
    ".settings.toml",  # local - git ignored
    ".secrets.toml",  # local - git ignored
)

# Environment constants
Environments = namedtuple(
    "Environments", ["default", "local", "development", "staging", "production"]
)
environment = Environments("default", "local", "development", "staging", "production")

# Load configuration using dyanconf
settings = Dynaconf(
    # Load envvars with prefix (e.g. 'APP_') or no prefix?
    envvar_prefix=False,
    # Load .env file
    load_dotenv=True,
    dotenv_override=False,  # Do not override exported env vars
    # Load files in order specified
    settings_files=[
        file_name_constants.file_name_settings,  # defaults
        file_name_constants.file_name_settings_local,
        file_name_constants.file_name_secrets_local,
    ],
    # Use environments
    environments=True,
    # Environment for default/fallback values
    default_env=environment.default,
    # Environment active
    env=environment.local,
    # Ignore unknown environment variables
    ignore_unknown_envvars=True,
)


# config class
class Configuration:

    @staticmethod
    def validate():

        logger.info(f"root_dir: '{root_dir}'")
        logger.info(f"config_dir: '{config_dir}'")

        # check Kubernetes runtime environment
        kubernetes_service_host = os.environ.get("KUBERNETES_SERVICE_HOST")
        logger.debug(f"OS ENV: KUBERNETES_SERVICE_HOST={kubernetes_service_host}")
        if kubernetes_service_host is None:
            logger.info("Not running in Kubernetes - local settings in files")
            Configuration.__validate_setting_files()
        else:
            logger.info("Running in Kubernetes - local settings in ConfigMap")

        # Settings required
        Configuration.__validate_required_settings_logging()
        Configuration.__validate_required_settings_s3()
        Configuration.__validate_required_settings_llm()
        Configuration.__validate_required_settings_other()

        # Validate
        settings.validators.validate()

        # Output settings
        Configuration.__output_settings()

    @staticmethod
    def __validate_setting_files():

        # Validate config files exist
        validate_file_exists(os.path.join(root_dir, ".env"))
        validate_file_exists(
            os.path.join(config_dir, file_name_constants.file_name_settings)
        )

    @staticmethod
    def __validate_required_settings_logging():

        settings.validators.register(
            Validator("log_levels", must_exist=True, is_type_of=(list, tuple)),
            Validator(
                "log_level",
                must_exist=True,
                is_type_of=(str),
                len_min=1,
                is_in=settings.log_levels,
            ),
            Validator("log_json", must_exist=True, is_type_of=(bool)),
            Validator("log_file", must_exist=True, is_type_of=(str), len_min=1),
            Validator(
                "log_file_rotation", must_exist=True, is_type_of=(str), len_min=1
            ),
            Validator(
                "log_file_retention_days", must_exist=True, is_type_of=(int), gt=0
            ),
        )

    @staticmethod
    def __validate_required_settings_s3():
        
        # Secrets
        settings.validators.register(
            Validator("s3_access_key_id", must_exist=True, is_type_of=(str), len_min=1),
            Validator(
                "s3_secret_access_key", must_exist=True, is_type_of=(str), len_min=1
            ),
        )

        # Other
        settings.validators.register(
            Validator("s3_bucket_name", must_exist=True, is_type_of=(str), len_min=1),
            Validator("s3_url", must_exist=True, is_type_of=(str), len_min=1),
        )

    @staticmethod
    def __validate_required_settings_llm():

        settings.validators.register(
            Validator("llm_names", must_exist=True, is_type_of=(list, tuple)),
            Validator(
                "llm_name",
                must_exist=True,
                is_type_of=(str),
                len_min=1,
                is_in=settings.llm_names,
            ),
        )

        settings.validators.register(
            Validator("llm_url_gemini", must_exist=True, is_type_of=(str), len_min=1), #TODO remove references to gemini
            Validator("llm_url_ollama", must_exist=True, is_type_of=(str), len_min=1),
            Validator("llm_url_llamacpp", must_exist=True, is_type_of=(str), len_min=1),
            Validator("llm_prompts_steps", must_exist=True, is_type_of=(int), gt=0),
        )
        if settings.llm_name == constants.LLM_NAME_GEMINI:
            settings.validators.register(
                Validator("llm_key", must_exist=True, is_type_of=(str), len_min=1),
            )
        else:
            settings.validators.register(
                Validator(
                    "llm_key", must_exist=True, is_type_of=(str), len_eq=0  # Empty
                ),
            )

    @staticmethod
    def __validate_required_settings_other():
        """Validate other settings."""

        # Flask
        settings.validators.register(
            Validator("flask_host", must_exist=True, is_type_of=(str), len_min=1),
            Validator("flask_port", must_exist=True, is_type_of=(int), gt=0),
        )

        # App
        settings.validators.register(
            Validator(
                "background_sleep_seconds", must_exist=True, is_type_of=(int), gt=0
            )
        )

    @staticmethod
    def __output_settings():

        logger.info(f"settings.env_for_dynaconf: {settings.env_for_dynaconf}")
        logger.info(f"settings.log_level: {settings.log_level}")
        logger.info(f"settings.log_json: {settings.log_json}")
        logger.info(f"settings.log_file: {settings.log_file}")
        logger.info(f"settings.log_file_rotation: {settings.log_file_rotation}")
        logger.info(
            f"settings.log_file_retention_days: {settings.log_file_retention_days}"
        )
        logger.info(f"settings.s3_access_key_id: {settings.s3_access_key_id}")
        logger.info("settings.s3_secret_access_key: *")
        logger.info(f"settings.s3_url: {settings.s3_url}")
        logger.info(f"settings.s3_bucket_name: {settings.s3_bucket_name}")
        logger.info(f"settings.llm_names: {settings.llm_names}")
        logger.info(f"settings.llm_name: {settings.llm_name}")
        logger.info(f"settings.llm_url_gemini: {settings.llm_url_gemini}")
        logger.info(f"settings.llm_url_ollama: {settings.llm_url_ollama}")
        logger.info(f"settings.llm_url_llamacpp: {settings.llm_url_llamacpp}")
        logger.info("settings.llm_key: *")
        logger.info(f"settings.llm_prompts_steps: {settings.llm_prompts_steps}")
        logger.info(f"settings.flask_host: {settings.flask_host}")
        logger.info(f"settings.flask_port: {settings.flask_port}")
        logger.info(
            f"settings.background_sleep_seconds: {settings.background_sleep_seconds}"
        )
