import sqlite3
from models.database_models import TRANSLATION_RECORDS_TABLE, USER_CONFIG_TABLE, CACHE_STATS_TABLE
import os

db_path = os.path.join(os.path.dirname(__file__), 'ai_translator.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(TRANSLATION_RECORDS_TABLE)
cursor.execute(USER_CONFIG_TABLE)
cursor.execute(CACHE_STATS_TABLE)
conn.commit()
conn.close()

print("数据库表已初始化。") 