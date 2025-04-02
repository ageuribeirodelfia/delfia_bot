from waitress import serve
from src import create_app
from src.config import Config
from src.logger import JsonLogger
from flask import Flask


app = create_app()

logger = JsonLogger()

config = Config()


if __name__ == "__main__":
    port = 8080
    logger.log_info(f"Server running on port: {port}")
    app.run(debug=True, port=8080, use_reloader=False)
