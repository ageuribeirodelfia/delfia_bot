import logging
import json
import os
from datetime import datetime
from pymongo import MongoClient


class JsonLogger:
    """Classe para formatar logs em JSON e salvar no MongoDB."""

    def __init__(self, log_file="logs/app.json", mongo_uri="mongodb://localhost:27017/", db_name="rpa_telmex_db", collection_name="logs"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Configuração do logger
        self.logger = logging.getLogger("JsonLogger")
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)

            file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
            file_handler.setFormatter(self.JsonFormatter())
            self.logger.addHandler(file_handler)

        # Configuração do MongoDB
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[db_name]
        self.mongo_collection = self.mongo_db[collection_name]

    class JsonFormatter(logging.Formatter):
        """Classe para formatar logs como JSON."""

        def format(self, record):
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "process": record.process,
                "thread": record.thread,
                "processName": record.processName,
                "threadName": record.threadName,
                "pathname": record.pathname,
                "filename": record.filename
            }

            # Adiciona dados extras ao log
            if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
                log_entry.update(record.extra_data)

            return json.dumps(log_entry, ensure_ascii=False)

    def _log(self, level, message, extra_data=None):
        """Método interno para logar mensagens."""
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "extra_data": extra_data
        }

        # Log no arquivo JSON
        self.logger.log(getattr(logging, level.upper()),
                        message, extra={"extra_data": extra_data})

        # Inserir log no MongoDB
        self.mongo_collection.insert_one(log_record)

    def log_info(self, message, extra_data=None):
        """Log para informações."""
        self._log("INFO", message, extra_data)

    def log_error(self, message, extra_data=None):
        """Log para erros."""
        self._log("ERROR", message, extra_data)

    def log_warning(self, message, extra_data=None):
        """Log para avisos."""
        self._log("WARNING", message, extra_data)

    def log_critical(self, message, extra_data=None):
        """Log para eventos críticos."""
        self._log("CRITICAL", message, extra_data)

    def log_debug(self, message, extra_data=None):
        """Log para depuração."""
        self._log("DEBUG", message, extra_data)
