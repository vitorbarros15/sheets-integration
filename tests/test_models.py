"""
Testes para os modelos de dados.
"""
import pytest
from pydantic import ValidationError

from app.models.sheet_models import SheetInput, SheetResponse, SheetRecord


class TestSheetInput:
    
    def test_valid_input(self):
        data = SheetInput(
            name="João Silva",
            serie=3,
            initial_weight="75kg",
            date="2024-01-15"
        )
        
        assert data.name == "João Silva"
        assert data.serie == 3
        assert data.initial_weight == "75kg"
        assert data.date == "2024-01-15"
    
    def test_name_validation(self):
        """Testa validação do nome."""
        with pytest.raises(ValidationError):
            SheetInput(
                name="A",
                serie=3,
                initial_weight="75kg",
                date="2024-01-15"
            )
        
        with pytest.raises(ValidationError):
            SheetInput(
                name="A" * 101,
                serie=3,
                initial_weight="75kg",
                date="2024-01-15"
            )
    
    def test_name_capitalization(self):
        """Testa capitalização automática do nome."""
        data = SheetInput(
            name="joão silva santos",
            serie=3,
            initial_weight="75kg",
            date="2024-01-15"
        )
        
        assert data.name == "João Silva Santos"
    
    def test_serie_validation(self):
        """Testa validação da série."""
        with pytest.raises(ValidationError):
            SheetInput(
                name="João Silva",
                serie=0,
                initial_weight="75kg",
                date="2024-01-15"
            )
        
        with pytest.raises(ValidationError):
            SheetInput(
                name="João Silva",
                serie=-1,
                initial_weight="75kg",
                date="2024-01-15"
            )
    
    def test_weight_validation(self):
        """Testa validação do peso."""
        valid_weights = ["75kg", "65.5kg", "80kg", "70.25kg"]
        for weight in valid_weights:
            data = SheetInput(
                name="João Silva",
                serie=3,
                initial_weight=weight,
                date="2024-01-15"
            )
            assert data.initial_weight == weight
        
        invalid_weights = ["75", "kg", "75g", "75.kg", "kg75", "75 kg"]
        for weight in invalid_weights:
            with pytest.raises(ValidationError):
                SheetInput(
                    name="João Silva",
                    serie=3,
                    initial_weight=weight,
                    date="2024-01-15"
                )
    
    def test_date_validation(self):
        """Testa validação da data."""
        valid_dates = ["2024-01-15", "2023-12-31", "2024-02-29"]
        for date in valid_dates:
            data = SheetInput(
                name="João Silva",
                serie=3,
                initial_weight="75kg",
                date=date
            )
            assert data.date == date
        
        invalid_dates = ["15-01-2024", "2024/01/15", "invalid", "2024-13-01", "2024-02-30"]
        for date in invalid_dates:
            with pytest.raises(ValidationError):
                SheetInput(
                    name="João Silva",
                    serie=3,
                    initial_weight="75kg",
                    date=date
                )


class TestSheetResponse:
    """Testes para o modelo SheetResponse."""
    
    def test_valid_response(self):
        """Testa resposta válida."""
        response = SheetResponse(
            status="success",
            message="Operação realizada com sucesso",
            data={"key": "value"}
        )
        
        assert response.status == "success"
        assert response.message == "Operação realizada com sucesso"
        assert response.data == {"key": "value"}
    
    def test_minimal_response(self):
        """Testa resposta mínima."""
        response = SheetResponse(status="success")
        
        assert response.status == "success"
        assert response.message is None
        assert response.data is None


class TestSheetRecord:
    """Testes para o modelo SheetRecord."""
    
    def test_valid_record(self):
        """Testa registro válido."""
        record = SheetRecord(
            name="João Silva",
            serie=3,
            initial_weight="75kg",
            date="2024-01-15"
        )
        
        assert record.name == "João Silva"
        assert record.serie == 3
        assert record.initial_weight == "75kg"
        assert record.date == "2024-01-15" 