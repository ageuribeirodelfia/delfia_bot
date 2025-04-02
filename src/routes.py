import flask
import json
import os
from src.logger import JsonLogger
from src.validators import validate_params
from src.controllers.rpa_controller import RPAController
from src.config import Config

routes = flask.Blueprint("routes", __name__)

config = Config()
logger = JsonLogger()

# Verificação de carregamento das configurações
logger.log_info(f"Configurações carregadas: BASE_URL={config.base_url}, STATUS_URL={config.status_url}, ISSUE_URL={config.issue_url}")

try:
    # Checando se a URL da rota está configurada corretamente
    if not config.status_url:
        raise ValueError("STATUS_URL não configurada corretamente no arquivo config.cfg.")
    
    logger.log_info(f"Registrando rota em: {config.status_url}")

    @routes.route(config.status_url, methods=["GET", "POST", "PUT"])
    def home():
        os.system("cls" if os.name == "nt" else "clear")

        if flask.request.method == 'GET':
            status = flask.request.args.get("status")
            issue_id = flask.request.args.get("issue_id")
            logger.log_info(f"status: {status}, issue_id: {issue_id}")
        else:
        
            try:
                issue_info = flask.request.get_json(silent=True)

                if issue_info is None:
                    raise ValueError("JSON inválido ou ausente.")
                status = issue_info.get('status')
                issue_id = issue_info.get('issueID')
            except Exception as e:
                logger.log_error(f"Erro ao processar JSON: {str(e)}")
                return "Erro ao processar JSON", 400
        logger.log_info(f"status: {status}, issue_id: {issue_id}")
        is_valid, error_msg, status_code = validate_params( issue_id, status, issue_info)
        if not is_valid:
            logger.log_error(error_msg)
            return error_msg, status_code

        RPAController.save_issue(issue_id, status, issue_info)
        return "OK", 200

except Exception as e:
    logger.log_info(f"Erro ao registrar a rota {e}")