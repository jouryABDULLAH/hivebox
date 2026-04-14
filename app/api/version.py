from fastapi import APIRouter
from app.core.config import settings 

router = APIRouter()

@router.get('/version')
def version():
    return {'version': settings.APP_VERSION}