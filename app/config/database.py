from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

DATABASE_NAME = os.getenv("DATABASE_NAME")
MONGO_URI = os.getenv("MONGO_URI")


# ---------------------------------------------------------
# MongoDB Connection
# ---------------------------------------------------------

client = MongoClient(
    MONGO_URI,
    server_api=ServerApi("1")
)

db = client[DATABASE_NAME]


# ---------------------------------------------------------
# Collections
# ---------------------------------------------------------

user_collection = db["users"]

trade_collection = db["trades"]

demo_account_collection = db["demo_accounts"]


# ---------------------------------------------------------
# User Index
# ---------------------------------------------------------

user_collection.create_index(
    [("email", 1)],
    unique=True
)


# ---------------------------------------------------------
# Database Getters
# ---------------------------------------------------------

def get_db():
    return db


def get_user_collection():
    return user_collection


def get_trade_collection():
    return trade_collection


def get_demo_account_collection():
    return demo_account_collection


# ---------------------------------------------------------
# Test MongoDB Connection
# ---------------------------------------------------------

try:

    client.admin.command("ping")

    print("✅ Connected to MongoDB")

except Exception as e:

    print("❌ MongoDB Connection Failed")

    print(e)