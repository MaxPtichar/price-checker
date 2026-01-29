import os

from dotenv import load_dotenv

load_dotenv()


class CONFIG:
    DB_NAME = os.getenv("DB_NAME")
    if not DB_NAME:
        raise ValueError("CRITICAL ERROR: DB_NAME is not set in .env file!")

    batch_size = int(os.getenv("batch_size", 10))
    start_id = int(os.getenv("start_id", 1))
    total_to_parse = int(os.getenv("total_to_parse", 10))
    semaphore_limit = int(os.getenv("semaphore_limit", 5))
    User_Agent = os.getenv("User_Agent", "MyParser/1.0")

    # headers
    headers = {"User-Agent": User_Agent}
