#!/usr/bin/python3

from modules.imessage_parser import get_messages
from modules.contacts_parser import get_contacts
from modules.report_generator import (
    export_to_csv,
    export_to_pdf
)
from modules.expense_parser import extract_expenses

# Step 1: Get messages (filtered by sender if configured)
messages = get_messages()

# Step 2: Extract expenses
expenses = extract_expenses(messages)

# Step 3: Export results
export_to_csv(expenses)
# export_to_pdf(expenses)

print("Expense tracking complete! 🚀")