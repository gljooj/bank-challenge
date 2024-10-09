import pytest
from unittest.mock import patch, MagicMock
from app import create_app


@patch('app.Scheduler')
@patch('app.setup_webhook')
@patch('app.Project')
def test_app_initialization(mock_project, mock_setup_webhook, mock_scheduler):

    project_mock = MagicMock()
    mock_project.return_value = project_mock

    mock_setup_webhook.return_value = None

    scheduler_mock = MagicMock()
    mock_scheduler.return_value = scheduler_mock

    app = create_app()

    mock_project.assert_called_once_with(
        environment="sandbox",
        id='project_id',
        private_key='private_key'
    )

    mock_setup_webhook.assert_called_once_with(app, project_mock)

    mock_scheduler.assert_called_once_with(project_mock)
    scheduler_mock.setup_scheduler.assert_called_once()
