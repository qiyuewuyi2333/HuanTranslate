import sqlite3
from flask import g
from config.settings import Config
import os

def get_db():
    if 'db' not in g:
        db_path = os.path.join(os.path.dirname(__file__), '..', 'ai_translator.db')
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
