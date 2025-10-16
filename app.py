from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "expenses.txt"

# Function to load expenses from file
def load_expenses():
    expenses = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    continue
                date, category, amount = parts
                try:
                    expenses.append({
                        "date": date,
                        "category": category,
                        "amount": float(amount)
                    })
                except ValueError:
                    continue
    return expenses

# Function to save expenses
def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        for exp in expenses:
            file.write(f"{exp['date']},{exp['category']},{exp['amount']}\n")

@app.route("/")
def index():
    expenses = load_expenses()
    total = sum(exp["amount"] for exp in expenses)
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date = request.form.get("date") or datetime.now().strftime("%d/%m/%Y")
        category = request.form.get("category")
        amount = request.form.get("amount")

        try:
            amount = float(amount)
        except ValueError:
            return redirect(url_for("index"))

        expenses = load_expenses()
        expenses.append({"date": date, "category": category, "amount": amount})
        save_expenses(expenses)
        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/delete/<int:index>")
def delete(index):
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        del expenses[index]
        save_expenses(expenses)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
