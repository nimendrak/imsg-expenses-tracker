#!/usr/bin/python3

from configs.packages import *
from configs.constants import (
    BANK_RULES,
    CATEGORY_RULES
)

def categorize_expense(expense):
    """
    Categorizes an expense based on keywords in its message.
    Returns a tuple (main_category, sub_category).
    If no rule matches, returns ("Other", "Other").
    """
    text = expense.get("message", "")
    text_lower = text.lower()

    # Iterate through each main category and its rules.
    for main_cat, rules in CATEGORY_RULES.items():
        # Sort main category keywords by length (longest first) for specificity.
        main_keywords = sorted(rules.get("keywords", []), key=len, reverse=True)
        for keyword in main_keywords:
            # Use regex word boundaries for exact matching.
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, text_lower):
                # If main category is found, try to determine a subcategory.
                subcat_found = None
                subcategories = rules.get("subcategories", {})
                for subcat, sub_keywords in subcategories.items():
                    sorted_sub_keywords = sorted(sub_keywords, key=len, reverse=True)
                    for sub_kw in sorted_sub_keywords:
                        sub_pattern = r'\b' + re.escape(sub_kw.lower()) + r'\b'
                        if re.search(sub_pattern, text_lower):
                            subcat_found = subcat
                            break
                    if subcat_found:
                        break
                if not subcat_found:
                    subcat_found = "General"
                return main_cat, subcat_found
    return "Other", "Other"

def extract_expenses(messages):
    expenses = []
    
    for msg in messages:
        # Normalize sender: remove extra spaces, carriage returns, and convert to uppercase.
        sender = msg.get("sender", "").strip().replace("\r", "").upper()
        text = msg.get("text", "")
        
        # Check if there are specific bank rules for this sender
        if sender in BANK_RULES:
            rules = BANK_RULES[sender]
            # Skip message if it contains any discard keywords.
            if any(kw.lower() in text.lower() for kw in rules.get("discard_keywords", [])):
                continue  # Skip this message
            
            # Use the bank's regex patterns to extract expense amounts.
            for pattern in rules.get("regex_patterns", []):
                matches = re.findall(pattern, text)
                for match in matches:
                    expense = {
                        "date": msg.get("date"),
                        "amount": match,
                        "transaction_type": "Debit" if "debit" in text.lower() else "Credit",
                        "message": text,
                        "sender": sender
                    }
                    # Categorize the expense.
                    main_cat, sub_cat = categorize_expense(expense)
                    expense["category"] = main_cat
                    expense["subcategory"] = sub_cat
                    expenses.append(expense)
        else:
            # Optionally handle messages from senders without specific bank rules.
            pass

    return expenses