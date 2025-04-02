from src.logger import JsonLogger
from src.repository.dataBase import DataBase
from src.controllers.queue_controller import QueueController


logger = JsonLogger()

class RPAController:
    @staticmethod
    def save_issue(issue_id, status, issue_info):
        logger.log_info(f"Salvando dados do incdente: ID={issue_id}, Status={status}, Body={issue_info}")

        # Adicionando a operação ao issue_info
        operation = issue_info.get("operation")
        if not operation:
            logger.log_error(f"Operação não especificada para o chamado {issue_id}")
            return "Erro: Operação não foi especificada.", 400

        # Enviar para a fila do celery
        QueueController.delay(issue_id, status, issue_info) 

        return "Chamado enviado para processamento", 200