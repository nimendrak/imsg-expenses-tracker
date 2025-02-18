#!/usr/bin/python3

from configs.packages import *

def export_to_csv(expenses, filename="output/expenses.csv", output_dir="output"):
    print("Exporting expenses to CSV...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.DataFrame(expenses)
    df.to_csv(filename, index=False)
    print(f"Expenses saved to {filename}")

def export_to_pdf(expenses, filename="output/expenses_report.pdf", output_dir="output"):
    print("Exporting expenses to PDF...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.DataFrame(expenses)
    html = df.to_html()
    pdfkit.from_string(html, filename)
    print(f"Expense report saved to {filename}")