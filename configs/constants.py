#!/usr/bin/python3

from configs.packages import *  

USERNAME = 'nimendra'
CHAT_DB_PATH = f'/Users/{USERNAME}/Library/Messages/chat.db'

# Example target senders (if you need an overall sender filter)
TARGET_SENDERS = ["COMBANK"]

# Bank-specific rules: For each bank, define regex patterns and keywords for messages to discard
BANK_RULES = {
    "COMBANK": {
        # Patterns to capture expense amounts.
        "regex_patterns": [
            r'(?i)(Rs\.?\s?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d{1,2})?)', # e.g., Rs 2800.00 or Rs. 1,500,000.00
            r'(?i)(LKR\s?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d{1,2})?)', # e.g., LKR 5.00, LKR 1,500.00
            r'(?i)(\$\d+(?:,\d{3})*(?:\.\d{1,2})?)', # e.g., $5.00, $1,500.00
        ],
        # Keywords that indicate a message should be discarded (e.g., failed transactions or OTPs)
        "discard_keywords": [
            "rejected", "technical failure", "otp", "failed"
        ]
    },
    # Add rules for other banks similarly:
    # "OTHERBANK": { ... }
}

CATEGORY_RULES = {
    "Bills & Home": {
        "keywords": ["bill", "rent", "home", "electricity", "water"],
        "subcategories": {
            "Utilities": ["electricity", "water", "gas"],
            "Rent": ["rent"],
            "Maintenance": ["maintenance", "repair"]
        }
    },
    "Food & Dining": {
        "keywords": ["UBER EATS"],
        "subcategories": {
            "Dining Out": ["UBER EATS"],
            "Groceries": []
        }
    },
    "Transportation": {
        "keywords": ["PICKME", "UBER"],
        "subcategories": {
            "Taxi": ["PICKME", "UBER"],
            "Public": []
        }
    },
    "Healthcare & Wellness": {
        "keywords": ["hospital", "doctor", "medicine", "health", "wellness", "clinic"],
        "subcategories": {
            "Medical": ["hospital", "doctor", "clinic"],
            "Pharmacy": ["medicine", "pharmacy"],
            "Wellness": ["gym", "fitness", "wellness"]
        }
    },
    "Personal & Lifestyle": {
        "keywords": ["clothing", "beauty", "fashion", "personal", "lifestyle"],
        "subcategories": {
            "Clothing": ["clothing", "apparel"],
            "Beauty": ["beauty", "cosmetic"],
            "Fitness": ["gym", "fitness"]
        }
    },
    "Fun Buffer": {
        "keywords": ["entertainment", "movie", "concert", "fun", "hobby"],
        "subcategories": {
            "Entertainment": ["movie", "concert", "theater"],
            "Hobbies": ["game", "hobby", "sport"]
        }
    }
}

ALL_MESSAGES = True  
MESSAGE_LIMIT = 10