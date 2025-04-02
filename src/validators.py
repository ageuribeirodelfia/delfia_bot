VALID_STATUS = ["Aberta",
                "Tratada",
                "Agendado",
                "Chegada",
                "Inicio",
                "Término",
                "Obs",
                "FinalSiebel",
                "Resolvido"
                ]

def validate_params(status, issue_id):
    if not status or not issue_id:
        return False, "parâmetros issue_id e status são requeridos", 400
    
    if status not in VALID_STATUS:
        return False, "Invalid status", 400
    
    return True, None, 200