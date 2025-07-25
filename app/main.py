"""
Aplicação principal da API de integração com Google Sheets.
"""
import logging
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routes.sheets_routes import router as sheets_router


def setup_logging():
    log_dir = Path(settings.log_file).parent
    log_dir.mkdir(exist_ok=True)
    
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(settings.log_file, encoding='utf-8')
    ]
    
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format=log_format,
        handlers=handlers
    )
    
    logger = logging.getLogger("app")
    logger.info("Sistema de logging configurado")


setup_logging()
logger = logging.getLogger("app")

app = FastAPI(
    title="Sheets Integration API",
    description="API REST para integração com planilhas do Google Sheets",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global para exceções não tratadas."""
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Erro interno do servidor",
            "detail": str(exc) if settings.debug else "Erro interno"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handler para exceções HTTP."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.on_event("startup")
async def startup_event():
    """Evento executado no início da aplicação."""
    logger.info("🚀 Iniciando Sheets Integration API")
    logger.info(f"📊 Planilha configurada: {settings.sheet_name}")
    logger.info(f"🔧 Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado no encerramento da aplicação."""
    logger.info("🛑 Encerrando Sheets Integration API")


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de verificação de saúde da API."""
    return {
        "status": "healthy",
        "service": "Sheets Integration API",
        "version": "1.0.0"
    }


app.include_router(sheets_router, prefix="/sheets", tags=["Sheets"])

logger.info("✅ Aplicação configurada com sucesso")