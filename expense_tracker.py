from datetime import datetime


def load_expenses():
    expenses = []
    try:
        with open("expenses.txt", "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    date, name, amount_str, category = [part.strip() for part in line.split(" - ", 3)]
                    expenses.append({
                        "date": date,
                        "name": name,
                        "amount": float(amount_str.replace(",", "")),
                        "category": category,
                    })
                except ValueError:
                    pass
    except FileNotFoundError:
        pass
    return expenses


def save_expenses(expenses):
    with open("expenses.txt", "w") as file:
        for expense in expenses:
            file.write(
                f"{expense['date']} - {expense['name']} - {expense['amount']:,.0f} - {expense['category']}\n"
            )


print("Welcome to My Personal Expense Tracker")
name = input("What is your name? ")
print(f"Hello, {name}! Let's record your expenses.")

expenses = load_expenses()

while True:
    print("\n===== PERSONAL EXPENSE TRACKER =====")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. View spending by category")
    print("4. View monthly summary")
    print("5. Exit")
    choice = input("Choose an option (1-5): ")

    if choice == "5":
        print("Thank you for using My Personal Expense Tracker!")
        break

    if choice not in ["1", "2", "3", "4"]:
        print("Please choose a valid option.")
        continue

    if choice == "1":
        print("\n--- ADD NEW EXPENSE ---")
        expense_name = input("What did you spend money on? ")

        while True:
            try:
                amount = float(input("How much did you spend? "))
                if amount > 0:
                    break
                print("Amount must be greater than zero.")
            except ValueError:
                print("Please enter a valid number.")

        category = input("What category does this expense belong to? ")
        today = datetime.now().strftime("%d-%m-%Y")
        expense = {
            "date": today,
            "name": expense_name,
            "amount": amount,
            "category": category,
        }
        expenses.append(expense)
        save_expenses(expenses)
        print("\nExpense Recorded!")
        print(f"Expense: {expense_name}")
        print(f"Amount:  {amount:,.0f}")
        print(f"Category: {category}")

    elif choice == "2":
        print("\n--- ALL EXPENSES ---")
        if not expenses:
            print("No expenses recorded yet.")
        else:
            total = 0
            for expense in expenses:
                total += expense["amount"]
                print(
                    f"{expense['date']} - {expense['name']} - UGX {expense['amount']:,.0f} - {expense['category']}"
                )
            print(f"\nTotal expenses: UGX {total:,.0f}")

    elif choice == "3":
        print("\n--- SPENDING BY CATEGORY ---")
        categories = {}
        for expense in expenses:
            category = expense["category"]
            categories[category] = categories.get(category, 0) + expense["amount"]

        if not categories:
            print("No expenses recorded yet.")
        else:
            for category, total in categories.items():
                print(f"{category}: UGX {total:,.0f}")

    elif choice == "4":
        print("\n--- MONTHLY SPENDING SUMMARY ---")
        monthly_totals = {}
        for expense in expenses:
            month = datetime.strptime(expense["date"], "%d-%m-%Y").strftime("%B %Y")
            monthly_totals[month] = monthly_totals.get(month, 0) + expense["amount"]

        if not monthly_totals:
            print("No expenses recorded yet.")
        else:
            for month, total in monthly_totals.items():
                print(f"{month}: UGX {total:,.0f}")
