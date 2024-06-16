import asyncio
import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from aiohttp import ClientSession, ClientConnectorError, ClientResponseError
from .config import CREATE_URL, BASE_URL, HEADERS
from .logger import logger

router = APIRouter()

# 异步创建任务，增加重试机制
@router.post("/create")
async def create_task(request: Request):
    try:
        payload = await request.json()
        logger.info(f"Received payload for task creation: {payload}")

        # 获取请求头中的 Authorization 字段
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logger.error("Authorization header is missing")
            raise HTTPException(status_code=400, detail="Authorization header is missing")

        # 将 Authorization 字段的值作为 Cookie 请求头的值
        headers = HEADERS.copy()
        headers["Cookie"] = auth_header

        retry_attempts = 5
        retry_delay = 2  # 初始等待时间（秒）

        for attempt in range(retry_attempts):
            try:
                async with ClientSession() as session:
                    async with session.post(CREATE_URL, headers=headers, json=payload) as response:
                        logger.info(f"Response status: {response.status}")
                        response_text = await response.text()

                        if response.status == 201:
                            data = json.loads(response_text)
                            logger.info(f"Task created successfully: {data}")
                            return JSONResponse(content=data[0])
                        elif response.status == 429:
                            retry_after = int(response.headers.get("Retry-After", retry_delay))
                            logger.warning(f"Rate limit exceeded, retrying after {retry_after} seconds...")
                            await asyncio.sleep(retry_after)
                        else:
                            logger.error(f"Failed to create task: {response.status}")
                            return JSONResponse(content=json.loads(response_text), status_code=response.status)
            except ClientConnectorError as e:
                logger.error(f"Cannot connect to host: {str(e)}")
                raise HTTPException(status_code=502, detail=f"Cannot connect to host: {str(e)}")
            except ClientResponseError as e:
                logger.error(f"Response error: {str(e)}")
                raise HTTPException(status_code=e.status, detail=f"Response error: {str(e)}")
            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")
                raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

        # 如果重试次数用尽
        logger.error("Exceeded maximum retry attempts")
        raise HTTPException(status_code=429, detail="Exceeded maximum retry attempts")
    except json.JSONDecodeError:
        logger.error("Invalid JSON payload")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# 异步查询任务状态
@router.get("/status/{task_id}")
async def check_task_status(task_id: str):
    try:
        logger.info(f"Checking status for task ID: {task_id}")
        url = BASE_URL + task_id
        async with ClientSession() as session:
            async with session.get(url, headers=HEADERS) as response:
                logger.info(f"Response status: {response.status}")
                response_text = await response.text()
                return JSONResponse(content=json.loads(response_text), status_code=response.status)
    except ClientConnectorError as e:
        logger.error(f"Cannot connect to host: {str(e)}")
        raise HTTPException(status_code=502, detail=f"Cannot connect to host: {str(e)}")
    except ClientResponseError as e:
        logger.error(f"Response error: {str(e)}")
        raise HTTPException(status_code=e.status, detail=f"Response error: {str(e)}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
