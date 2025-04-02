import configparser
import time
from celery import Celery
from typing import Dict
from src.logger import JsonLogger
from src.repository.dataBase import DataBase

# Inicializando logge e banco de dados
logger = JsonLogger()
database = DataBase()

# Carregar configurações do arquivo config.cfg
logger.log_info("Carregando o arquivo de configuração.")
config = configparser.ConfigParser()
config.read("config.cfg")

# Configurando Celery e Redis
REDIS_URI = config.get("REDIS", "REDIS_URI")
celery = Celery(
    'task',
    backend=[REDIS_URI],
    worker=[REDIS_URI]
)

@celery.task()
def process_incident(data: Dict):

    """
    Processa incidentes enviados para a fila de execução
    """
    operation = data.get("operation")
    issue_id = data.get("issue_id")
    logger.log_info(f"Processando incidente ID: {issue_id}, operação: {operation}")
    try:

        if operation == "TMX":
            from src.rpa.siebel_telmex import SiebelTelmex
            SiebelTelmex(data)
        elif operation == "BOT":
            from src.rpa.siebel_boticario import SiebelBoticario
            SiebelBoticario(data)
        else:
            raise ValueError("Operação desconhecida")
        status = "Processado"
    except Exception as e:
        logger.log_error(f"Erro ao processar incidente {issue_id}: {str(e)}")
        status = "Error"

    # Salvar status do incidente no MongoDB
    database.update_value("issue_id", issue_id, issue_id, {"$set": {"status_processing":status}})
    logger.log_info(f"incidente {issue_id} atualizado no banco de dados com status {status}.")
    return status

class QueueController:
    @staticmethod
    def add_to_queue(data: Dict):
        """
        Adiciona um novo incidente à fila de processamento.
        """

        issue_id = data.get("issue_id")

        # Registrar incidente no banco de dados antes de enviar à fila
        database.insert_incident_info(
            issueID=issue_id,
            fields=data.get("fields",{}),
            status_issue=data.get("statusJira", "Aberto"),
            status_processing="Na fila",
            date=time.strftime("%Y-%m-%d %H:%M:%S")
        )

        # Enviar para processamento assíncrono
        process_incident.apply_async(args=[data])
        logger.log_info(f"Incidente {issue_id} enviado para processamento.")