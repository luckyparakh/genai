from fastapi import FastAPI
import logging
from model import UserInput
from gitlab import get_data
from logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG) #reconfigures the entire logging system, including the root logger.
logger = logging.getLogger("api_logger")
app = FastAPI()


@app.post("/create-release-notes")
async def get_latest_tag(input_data: UserInput):
    logger.debug(f"User Input:{input_data}")
    await get_data(input_data, logger)
