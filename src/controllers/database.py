from pymongo import MongoClient
from configparser import ConfigParser


class MongoConfig:

    # Carregar arquivo de configuração
    config = ConfigParser()
    config.read("config.cfg")
    MONGO_URI = config.get("database", "MONGO_URI")
    LOG_FILE = config.get("logging", "LOG_FILE")

    # Conexão com o MongoDB
    client = MongoClient(MONGO_URI)
    db = client["rpa_telmex_db"]
    collection = db['incidents']
