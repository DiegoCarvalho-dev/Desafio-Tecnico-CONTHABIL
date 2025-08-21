import os
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def upload_to_local_server(file_path: str) -> str:
    filename = os.path.basename(file_path)
    dest_path = UPLOAD_DIR / filename

    try:
        shutil.copy(file_path, dest_path)
        url = f"http://127.0.0.1:8001/files/{filename}"
        logger.info(f"Arquivo disponível em {url}")
        return url
    except Exception as e:
        logger.error(f"Erro no upload local: {e}")
        raise
