"""
Rotas da API para operações com Google Sheets.
"""
import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.models.sheet_models import SheetInput, SheetResponse, SheetRecord
from app.services.sheets_service import sheets_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/dados", response_model=List[SheetRecord])
async def list_data():
    """Lista todos os dados da planilha."""
    try:
        logger.info("Solicitação para listar dados recebida")
        records = sheets_service.get_all_records()
        
        if not records:
            logger.info("Nenhum registro encontrado na planilha")
            return []
        
        logger.info(f"Retornando {len(records)} registros")
        return records
        
    except Exception as e:
        logger.error(f"Erro ao listar dados: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao acessar a planilha: {str(e)}"
        )


@router.post("/adicionar", response_model=SheetResponse)
async def add_data(data: SheetInput):
    """Adiciona um novo registro à planilha."""
    try:
        logger.info(f"Solicitação para adicionar dados: {data.dict()}")
        
        success = sheets_service.append_row(data)
        
        if success:
            logger.info("Dados adicionados com sucesso")
            return SheetResponse(
                status="success",
                message="Dados adicionados com sucesso!",
                data=data.dict()
            )
        else:
            logger.error("Falha ao adicionar dados")
            raise HTTPException(
                status_code=500,
                detail="Falha ao adicionar dados à planilha"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao adicionar dados: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao adicionar dados à planilha: {str(e)}"
        )


@router.get("/status", response_model=SheetResponse)
async def check_status():
    """Verifica o status da conexão com Google Sheets."""
    try:
        logger.info("Verificando status da conexão")
        
        sheet = sheets_service.get_sheet()
        
        return SheetResponse(
            status="success",
            message="Conexão com Google Sheets OK",
            data={
                "sheet_title": sheet.title,
                "sheet_id": sheet.id
            }
        )
        
    except Exception as e:
        logger.error(f"Erro na verificação de status: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Erro de conectividade com Google Sheets: {str(e)}"
        )