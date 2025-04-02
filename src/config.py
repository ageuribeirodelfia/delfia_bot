import configparser
import os
from src.logger import JsonLogger

logger = JsonLogger()


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.path.join(
            os.path.dirname(__file__), '../config.cfg'))

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {config_path}")
        logger.log_error(f"Configurações carregadas de: {config_path}")
        self.config.read(config_path)

    # Database Configurations
    @property
    def mongo_uri(self):
        return self.config['DATABASE']['MONGO_URI']

    @property
    def db_name(self):
        return self.config['DATABASE']['DB_NAME']

    @property
    def collection_name(self):
        return self.config['DATABASE']['COLLECTION_NAME']

    # Logging Configurations
    @property
    def log_file(self):
        return self.config['LOGGING']['LOG_FILE']

    @property
    def log_level(self):
        return self.config['LOGGING']['LOG_LEVEL']

    # API Configurarion

    @property
    def base_url(self):
        return self.config['API']['BASE_URL']

    @property
    def status_url(self):
        return self.config['API']['STATUS_URL']

    @property
    def issue_url(self):
        return self.config['API']['ISSUE_URL']
