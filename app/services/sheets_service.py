"""
Serviço para integração com Google Sheets.
"""
import logging
from pathlib import Path
from typing import List, Dict, Any

import gspread
from gspread import Spreadsheet, Worksheet
from oauth2client.service_account import ServiceAccountCredentials

from app.config import settings
from app.models.sheet_models import SheetInput

logger = logging.getLogger(__name__)


class SheetsService:
    """Serviço para operações com Google Sheets."""
    
    def __init__(self):
        self._client = None
        self._sheet = None
    
    def _get_client(self) -> gspread.Client:
        if self._client is None:
            try:
                credentials_path = settings.get_credentials_path()
                
                if not credentials_path.exists():
                    raise FileNotFoundError(
                        f"Arquivo de credenciais não encontrado: {credentials_path}"
                    )
                
                scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
                
                logger.info(f"Autenticando com credenciais: {credentials_path}")
                creds = ServiceAccountCredentials.from_json_keyfile_name(
                    str(credentials_path), scope
                )
                self._client = gspread.authorize(creds)
                logger.info("Autenticação realizada com sucesso")
                
            except Exception as e:
                logger.error(f"Erro na autenticação: {str(e)}")
                raise
        
        return self._client
    
    def get_sheet(self, sheet_name: str = None) -> Worksheet:
        if sheet_name is None:
            sheet_name = settings.sheet_name
        
        try:
            client = self._get_client()
            logger.info(f"Abrindo planilha: {sheet_name}")
            spreadsheet = client.open(sheet_name)
            worksheet = spreadsheet.sheet1
            logger.info(f"Planilha {sheet_name} aberta com sucesso")
            return worksheet
            
        except gspread.SpreadsheetNotFound:
            logger.error(f"Planilha '{sheet_name}' não encontrada")
            raise Exception(f"Planilha '{sheet_name}' não encontrada. Verifique se o nome está correto e se foi compartilhada com a service account.")
        except Exception as e:
            logger.error(f"Erro ao abrir planilha: {str(e)}")
            raise
    
    def get_all_records(self, sheet_name: str = None) -> List[Dict[str, Any]]:
        try:
            sheet = self.get_sheet(sheet_name)
            records = sheet.get_all_records()
            logger.info(f"Obtidos {len(records)} registros da planilha")
            return records
        except Exception as e:
            logger.error(f"Erro ao obter registros: {str(e)}")
            raise
    
    def append_row(self, data: SheetInput, sheet_name: str = None) -> bool:
        try:
            sheet = self.get_sheet(sheet_name)
            line_new = [data.name, data.serie, data.initial_weight, data.date]
            
            logger.info(f"Adicionando linha: {line_new}")
            sheet.append_row(line_new)
            logger.info("Linha adicionada com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao adicionar linha: {str(e)}")
            raise


sheets_service = SheetsService()


def get_sheet(sheet_name: str = None) -> Worksheet:
    return sheets_service.get_sheet(sheet_name)


def append_row(sheet: Worksheet, data: SheetInput) -> None:
    sheets_service.append_row(data) 