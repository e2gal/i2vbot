#!/usr/bin/env python2

import os
import sqlite3

import util

DATA_FILE = "data/data.sqlite"

def initDB():
    with sqlite3.connect(DATA_FILE) as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS image_data (
            chat_id INT,
            post_id INT,
            time INT,
            rating TEXT,
            character TEXT,
            copyright TEXT,
            general TEXT,
            handler_used TEXT,
            PRIMARY KEY (chat_id, post_id))""")

def loadData(chat_id, post_id):
    if not os.path.exists(DATA_FILE):
        return None

    with sqlite3.connect(DATA_FILE) as con:
        cur = con.cursor()
        cur.execute("""
        SELECT rating, character, copyright, general
          FROM image_data
         WHERE chat_id = ? AND post_id = ?""", (chat_id, post_id))
        data = cur.fetchone()
        if data is None:
            return None

        return {
            "rating":    data[0],
            "character": set(util.splitOrEmpty(data[1], ",")),
            "copyright": set(util.splitOrEmpty(data[2], ",")),
            "general":   set(util.splitOrEmpty(data[3], ","))
        }

def saveData(chat_id, post_id, data):
    if not os.path.exists(DATA_FILE):
        initDB()

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
            chat_id, post_id, time, rating, character, copyright, general, handler_used)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (chat_id, post_id, time, rating, character, copyright, general, handler))