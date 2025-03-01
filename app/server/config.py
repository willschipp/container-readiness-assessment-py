import os

class Config:
    URL = "localhost:9000"
    KEY = "KEY"
    SECRET = "SECRET"
    LLM_URL = ""
    LLM_KEY = ""

    @classmethod
    def init_app(cls,app):
        pass

class LlamaCPPConfig(Config):
    URL = os.getenv("S3_URL","localhost:9000")
    KEY = os.getenv("KEY","gnSXfqewAZ8ptThQAF92")
    SECRET = os.getenv("SECRET")
    LLM_URL = os.getenv("LLAMACPP_URL","http://localhost:8080/completion")
    LLM_KEY = ""    


config = {
    'default': LlamaCPPConfig,
}