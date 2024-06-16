from fastapi import FastAPI
from luma.routes import router  # 使用绝对导入
from luma.logger import logger

app = FastAPI()

app.include_router(router)
