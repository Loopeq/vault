from api.v1 import router as v1_router
from core.setup import create_application

app = create_application(router=v1_router)
