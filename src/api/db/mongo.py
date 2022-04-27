from motor import motor_asyncio, MotorCollection

client = motor_asyncio.AsyncIOMotorClient()
db = client["account_book"]
users_coll = db["users"]

