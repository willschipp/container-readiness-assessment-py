import server.constants as constants
from server.configuration import settings


class Config:
    s3_bucket = settings.s3_bucket_name
    s3_url = settings.s3_url
    s3_access_key_id = settings.s3_access_key_id
    s3_secret_access_key = settings.s3_secret_access_key
    llm_url = '' # Set in sub class
    llm_key = settings.llm_key

    @classmethod
    def init_app(cls, app):
        """Initialize app"""
        pass

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: The string representation of the object.
        """
        return f"{__class__.__name__}: s3_bucket={self.s3_bucket_name}, s3_url={self.s3_url}, s3_access_key_id={self.s3_access_key_id}, s3_secret_access_key=*, llm_url={self.llm_url}, llm_key=*"


class ConfigGemini(Config):
    llm_url = settings.llm_url_gemini


class ConfigOllama(Config):
    llm_url = settings.llm_url_ollama


class ConfigLlamaCPP(Config):
    llm_url = settings.llm_url_llamacpp


config = {
    constants.LLM_NAME_GEMINI: ConfigGemini,
    constants.LLM_NAME_OLLAMA: ConfigOllama,
    constants.LLM_NAME_LLAMACPP: ConfigLlamaCPP,
}