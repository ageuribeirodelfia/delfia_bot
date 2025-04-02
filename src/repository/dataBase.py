import logging
from pymongo import MongoClient
from src.config import Config
from src.logger import JsonLogger

logger = JsonLogger()


class DataBase:
    def __init__(self):
        config = Config()
        self.mongo_uri = config.mongo_uri
        self.db_name = config.db_name
        self.collection_name = config.collection_name

        client = MongoClient(self.mongo_uri)
        db = client[self.db_name]
        self.collection = db[self.collection_name]
        logger.log_info(
            f"Conectado ao banco de dados {self.db_name}, coleção {self.collection_name}"
        )

    def insert_incident_info(self, issue_id, fields, status_issue, status_processing, date):
        try:
            issue_info = {
                "id": issue_id,
                "fields": fields,
                "statusJira": status_issue,
                "status_processing": status_processing,
                "delivery_date": date
            }

            insert_id = self.collection.insert_one(issue_info).inserted_id
            logger.log_info(
                f"Os dados do chamado foram salvos no MongoDB. \n ID: {insert_id}")
            return insert_id
        except Exception as e:
            logger.log_error(
                f"ERRO: Não foi possível inserir as informações do chamado no banco de dados. Erro: {str(e)}")
            return None

    def update_value(self, key, value, insert_id, action):
        try:
            issue = {key: str(value)}
            myquery = {"_id": insert_id}
            newvalues = {action: issue}
            self.collection.update_one(myquery, newvalues)
            logger.log_info(
                f"Número do chamado atualizado no banco de dados. ID: {insert_id}")
            return insert_id
        except Exception as e:
            logger.log_error(
                f"ERRO: Não foi possivel atualizar o chamado {value} . Erro: {str(e)}")

    def select_one_processing(self, status):
        return self.collection.find_one({'status_processing': status})

    def select_all_processing(self, status):
        return self.conllection.find({'status_processing': status})

    def select_all_one_key(self, key, value, key1, value2):
        return self.collection.find({key: value, key1: value2})

    def select_complex_query(self, key_1, value_1, key_2, value_2, key_3, value_3):
        return self.collection.find_one({
            str(key_1): str(value_1),
            str(key_2): str(value_2),
            str(key_3): str(value_3)
        })

    def clean_data_base(self):
        answer = input(
            "Foi efetuado o download do JSON no MongoDB Compass para salvar como backup? (S/N): ").upper()
        if answer == "S":
            self.collection.delete_many({"status_processing": "PROCESSADO"})
            self.collection.delete_many({"status_processing": "FECHADO"})
            print("Limpeza efetuada com sucesso!")
        else:
            print("Processo de limpeza não efetuado!")
