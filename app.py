from time import sleep

from flask import Flask
from starkcore import Project
from webhook_handler import setup_webhook
from services.scheduler import Scheduler
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    private_key_content = os.getenv('STARKBANK_PRIVATE_KEY')
    project_id = os.getenv('STARKBANK_PROJECT_ID')

    project = Project(
        environment="sandbox",
        id=project_id,
        private_key=private_key_content
    )

    setup_webhook(app, project)
    Scheduler(project).setup_scheduler()

    return app


if __name__ == '__main__':
    try:

        flask_app = create_app()
        sleep(2)
        flask_app.run(host='0.0.0.0', port=5000, debug=True)

    except Exception as e:
        print(f"Error to start Flask: {e}")
