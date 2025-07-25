"""
Configurações e fixtures para os testes.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.main import app
from app.models.sheet_models import SheetInput


@pytest.fixture
def client():
    """Cliente de teste para a API."""
    return TestClient(app)


@pytest.fixture
def sample_sheet_input():
    """Dados de exemplo para teste."""
    return SheetInput(
        name="João Silva",
        serie=3,
        initial_weight="75kg",
        date="2024-01-15"
    )


@pytest.fixture
def sample_sheet_records():
    """Registros de exemplo da planilha."""
    return [
        {
            "name": "João Silva",
            "serie": 3,
            "initial_weight": "75kg",
            "date": "2024-01-15"
        },
        {
            "name": "Maria Santos",
            "serie": 5,
            "initial_weight": "65kg",
            "date": "2024-01-20"
        }
    ]


@pytest.fixture
def mock_worksheet():
    """Mock do worksheet do Google Sheets."""
    mock_sheet = Mock()
    mock_sheet.title = "Academia"
    mock_sheet.id = "1234567890"
    mock_sheet.get_all_records.return_value = [
        {
            "name": "João Silva",
            "serie": 3,
            "initial_weight": "75kg",
            "date": "2024-01-15"
        }
    ]
    mock_sheet.append_row.return_value = None
    return mock_sheet


@pytest.fixture
def mock_sheets_service(mock_worksheet):
    """Mock do serviço de sheets."""
    with patch('app.services.sheets_service.sheets_service') as mock_service:
        mock_service.get_sheet.return_value = mock_worksheet
        mock_service.get_all_records.return_value = mock_worksheet.get_all_records()
        mock_service.append_row.return_value = True
        yield mock_service 