import mysql.connector
from datetime import datetime, date, time
from decimal import Decimal
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': 'mysql-21d9f0f9-iisgalvanimi-8e81.b.aivencloud.com',
    'port': 13692,
    'user': 'avnadmin',
    'password': 'AVNS_xogXO8BBfCghY5AJ2nn',
    'database': 'Droni'
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Exception as e:
        print("❌ ERRORE CONNESSIONE DB:", e)
        return None

def to_json_safe(obj):
    if obj is None: return None
    if isinstance(obj, (Decimal, int, float)): return float(obj)
    if isinstance(obj, (datetime, date)): return obj.isoformat()
    if isinstance(obj, time): return obj.strftime('%H:%M:%S')
    if isinstance(obj, bytes): return obj.decode('utf-8')
    return str(obj)

def serialize_row(row):
    return {k: to_json_safe(v) for k, v in row.items()} if row else {}
