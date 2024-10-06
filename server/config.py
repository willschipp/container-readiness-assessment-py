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

class DevConfig(Config):
    URL = "localhost:9000"
    KEY = "gjUHI2lScQ6JhwnbBkas"
    SECRET = os.getenv("SECRET")
    LLM_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=API_KEY"
    LLM_KEY = os.getenv("LLM_KEY")


class OllamaConfig(Config):
    URL = "localhost:9000"
    KEY = "gjUHI2lScQ6JhwnbBkas"
    SECRET = os.getenv("SECRET")
    LLM_URL = "http://localhost:11434/api/generate"
    LLM_KEY = ""


config = {
    'dev': DevConfig,
    'ollama': OllamaConfig,
}