#!/usr/bin/python3

from configs.packages import *

def get_address_book_path():
    base_path = os.path.expanduser("~/Library/Application Support/AddressBook/Sources/")
    address_book_files = glob.glob(os.path.join(base_path, "*/AddressBook-v22.abcddb"))
    return address_book_files[0] if address_book_files else None

def get_contacts():
    address_book_path = get_address_book_path()
    if not address_book_path:
        return {}

    conn = sqlite3.connect(address_book_path)
    cursor = conn.cursor()

    query = """
    SELECT ZFIRSTNAME, ZLASTNAME, ZFULLNUMBER
    FROM ZABCDRECORD
    LEFT JOIN ZABCDPHONENUMBER ON ZABCDRECORD.Z_PK = ZABCDPHONENUMBER.ZOWNER
    """
    
    contacts = {}
    for first, last, number in cursor.execute(query).fetchall():
        if number:
            contacts[number.replace(" ", "").replace("-", "")] = f"{first} {last}".strip()
    
    conn.close()
    return contacts