#!/usr/bin/env python2

import os
import sqlite3

from config import DATA_FILE
import util

def init_db():
    with sqlite3.connect(DATA_FILE) as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS image_data (
            chat_id INT,
            file_id TEXT,
            time INT,
            rating TEXT,
            character TEXT,
            copyright TEXT,
            general TEXT,
            handler_used TEXT,
            PRIMARY KEY (chat_id, file_id))""")

def load_data(chat_id, file_id):
    if not os.path.exists(DATA_FILE):
        init_db()

    with sqlite3.connect(DATA_FILE) as con:
        cur = con.cursor()
        cur.execute("""
        SELECT rating, character, copyright, general
          FROM image_data
         WHERE chat_id = ? AND file_id = ?""", (chat_id, file_id))
        data = cur.fetchone()
        if data is None:
            return None

        return {
            "rating":    data[0],
            "character": set(util.split_or_empty(data[1], ",")),
            "copyright": set(util.split_or_empty(data[2], ",")),
            "general":   set(util.split_or_empty(data[3], ","))
        }

def save_data(chat_id, file_id, data):
    if not os.path.exists(DATA_FILE):
        init_db()

    rating    = data["rating"]
    character = ",".join(data["character"])
    copyright = ",".join(data["copyright"])
    general   = ",".join(data["general"])
    time      = int(data["time"])
    handler   = data["handler"]

    with sqlite3.connect(DATA_FILE) as con:
        cur = con.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO image_data (
            chat_id, file_id, time, rating, character, copyright, general, handler_used)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (chat_id, file_id, time, rating, character, copyright, general, handler))
