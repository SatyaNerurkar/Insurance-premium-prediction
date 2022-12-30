import os
import json
import pymongo
from dataclasses import dataclass
import pandas as pd

@dataclass
class EnvironmentVariable:
    # Provide the mongodb localhost url to connect python to mongodb.
    MONGO_DB_URL:str = os.getenv("MONGO_DB_URL")

env_var = EnvironmentVariable()

mongo_client = pymongo.MongoClient(env_var.MONGO_DB_URL)

TARGET_COLUMN = "expenses"