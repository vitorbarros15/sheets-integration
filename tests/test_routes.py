"""
Testes para as rotas da API.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


class TestSheetsRoutes:
    """Testes para as rotas de sheets."""
    
    def test_list_data_success(self, mock_sheets_service, sample_sheet_records):
        """Testa listagem de dados com sucesso."""
        mock_sheets_service.get_all_records.return_value = sample_sheet_records
        
        client = TestClient(app)
        response = client.get("/sheets/dados")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "João Silva"
        assert data[1]["name"] == "Maria Santos"
    
    def test_list_data_empty(self, mock_sheets_service):
        """Testa listagem quando não há dados."""
        mock_sheets_service.get_all_records.return_value = []
        
        client = TestClient(app)
        response = client.get("/sheets/dados")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    def test_list_data_error(self, mock_sheets_service):
        """Testa erro na listagem de dados."""
        mock_sheets_service.get_all_records.side_effect = Exception("Erro de conexão")
        
        client = TestClient(app)
        response = client.get("/sheets/dados")
        
        assert response.status_code == 500
        data = response.json()
        assert "Erro ao acessar a planilha" in data["detail"]
    
    def test_add_data_success(self, mock_sheets_service, sample_sheet_input):
        """Testa adição de dados com sucesso."""
        mock_sheets_service.append_row.return_value = True
        
        client = TestClient(app)
        response = client.post("/sheets/adicionar", json=sample_sheet_input.dict())
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Dados adicionados com sucesso!"
        assert data["data"]["name"] == "João Silva"
    
    def test_add_data_validation_error(self):
        """Testa erro de validação na adição de dados."""
        invalid_data = {
            "name": "A",  # Muito curto
            "serie": -1,  # Negativo
            "initial_weight": "invalid",  # Formato inválido
            "date": "invalid-date"  # Data inválida
        }
        
        client = TestClient(app)
        response = client.post("/sheets/adicionar", json=invalid_data)
        
        assert response.status_code == 422
    
    def test_add_data_service_error(self, mock_sheets_service, sample_sheet_input):
        """Testa erro no serviço ao adicionar dados."""
        mock_sheets_service.append_row.side_effect = Exception("Erro na planilha")
        
        client = TestClient(app)
        response = client.post("/sheets/adicionar", json=sample_sheet_input.dict())
        
        assert response.status_code == 500
        data = response.json()
        assert "Erro ao adicionar dados à planilha" in data["detail"]
    
    def test_check_status_success(self, mock_sheets_service, mock_worksheet):
        """Testa verificação de status com sucesso."""
        mock_sheets_service.get_sheet.return_value = mock_worksheet
        
        client = TestClient(app)
        response = client.get("/sheets/status")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Conexão com Google Sheets OK"
        assert data["data"]["sheet_title"] == "Academia"
    
    def test_check_status_error(self, mock_sheets_service):
        """Testa erro na verificação de status."""
        mock_sheets_service.get_sheet.side_effect = Exception("Erro de conexão")
        
        client = TestClient(app)
        response = client.get("/sheets/status")
        
        assert response.status_code == 503
        data = response.json()
        assert "Erro de conectividade com Google Sheets" in data["detail"] 