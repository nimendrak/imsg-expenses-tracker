#!/usr/bin/python3

from configs.packages import *
from configs.constants import (
    CHAT_DB_PATH,
    TARGET_SENDERS,
    ALL_MESSAGES,
    MESSAGE_LIMIT,
)

def get_messages():
    conn = sqlite3.connect(CHAT_DB_PATH)
    cursor = conn.cursor()
    
    query = """
    SELECT message.ROWID, message.date, message.text, handle.id, message.cache_roomnames
    FROM message
    LEFT JOIN handle ON message.handle_id = handle.ROWID
    WHERE message.text IS NOT NULL
    """
        
    params = []
    if TARGET_SENDERS:
        conditions = []
        for sender in TARGET_SENDERS:
            conditions.append(
                "(UPPER(TRIM(REPLACE(handle.id, char(13), ''))) = ? OR UPPER(TRIM(REPLACE(message.cache_roomnames, char(13), ''))) = ?)"
            )
            params.extend([sender.upper(), sender.upper()])
        query += " AND (" + " OR ".join(conditions) + ")"

    if not ALL_MESSAGES:
        query += " ORDER BY message.date DESC LIMIT ?"
        params.append(MESSAGE_LIMIT)

    results = cursor.execute(query, params).fetchall()

    messages = []
    for rowid, date, text, sender, roomname in results:
        apple_epoch_start = datetime.datetime(2001, 1, 1)
        new_date = apple_epoch_start + datetime.timedelta(seconds=date / 1000000000)
        messages.append({
            "id": rowid, 
            "date": new_date, 
            "text": text, 
            "sender": sender if sender else roomname  # fallback to roomname if sender is None
        })
    
    conn.close()
    
    return messages