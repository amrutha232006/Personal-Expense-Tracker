from database import create_database,get_connection
from datetime import date

def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than zero!")
            else:
                return amount

        except ValueError:
            print("Please enter a valid number!")


def get_valid_date():
    while True:
        transaction_date = input("Enter date (YYYY-MM-DD): ")

        try:
            return date.fromisoformat(transaction_date)

        except ValueError:
            print("Invalid date! Use YYYY-MM-DD format.")


def add_income():
    try:
        amount = get_valid_amount()
        category=input("Enter income category (Salary, Freelance, etc.): ")
        description=input("Enter description:")
        transaction_date = get_valid_date()

        conn=get_connection()
        cursor=conn.cursor()

        query="""
        insert into transactions
        (type,amount,category,description,transaction_date)
        values(%s,%s,%s,%s,%s)
        """

        values=("Income", amount,category,description,transaction_date)
        cursor.execute(query,values)
        conn.commit()

        print("Income added successfully")

    except ValueError:
        print("Please enter a valid amount:")

    except Exception as e:
        print("Error:",e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def add_expense():
    try:
        amount = get_valid_amount()
        category = input("Enter category (Food, Travel, Shopping, etc.): ")
        description = input("Enter description: ")
        transaction_date = get_valid_date()

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO transactions
        (type, amount, category, description, transaction_date)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = ("Expense", amount, category, description, transaction_date)
        cursor.execute(query, values)
        conn.commit()

        print("Expense added successfully!")

    except ValueError:
        print("Please enter a valid amount.")

    except Exception as e:
        print("Error:",e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def view_transactions():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM transactions
            ORDER BY transaction_date DESC
        """)

        records = cursor.fetchall()

        if not records:
            print("No transactions found!")
        else:
            print("\n========== ALL TRANSACTIONS ==========")

            for record in records:
                print("----------------------------------")
                print("ID:", record[0])
                print("Type:", record[1])
                print("Amount: ₹", record[2])
                print("Category:", record[3])
                print("Description:", record[4])
                print("Date:", record[5])

    except Exception as e:
        print("Error:",e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def search_transaction(): 
    try:
        transaction_id=int(input("Enter transaction ID:"))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM transactions WHERE id = %s",
            (transaction_id,)
        )

        record=cursor.fetchone()

        if record:
            print("\n========== TRANSACTION FOUND ==========")
            print("ID:", record[0])
            print("Type:", record[1])
            print("Amount: ₹", record[2])
            print("Category:", record[3])
            print("Description:", record[4])
            print("Date:", record[5])
        else:
            print("Transaction not found")

    except ValueError:
        print("Enter a valid transaction ID.")

    except Exception as e:
        print("Error:",e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def update_transaction():
    try:
        transaction_id = int(input("Enter Transaction ID to update: "))

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute(
            "SELECT * FROM transactions WHERE id = %s",
            (transaction_id,)
        )

        record = cursor.fetchone()

        if record:
            print("\nCurrent Transaction:")
            print("Type:", record[1])
            print("Amount:", record[2])
            print("Category:", record[3])
            print("Description:", record[4])
            print("Date:", record[5])

            print("\nEnter New Details:")

            transaction_type = input("New Type (Income/Expense): ").capitalize()
            amount = float(input("New Amount: "))
            category = input("New Category: ")
            description = input("New Description: ")
            transaction_date = input("New Date (YYYY-MM-DD): ")

            if transaction_type not in ("Income", "Expense"):
                print("Invalid type! Enter Income or Expense.")
                return

            query = """
            UPDATE transactions
            SET type = %s, amount = %s, category = %s,
                description = %s, transaction_date = %s
            WHERE id = %s
            """

            values = (
                transaction_type, amount, category,
                description, transaction_date, transaction_id
            )

            cursor.execute(query, values)
            conn.commit()

            print("Transaction updated successfully!")

        else:
            print("Transaction not found!")

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as e:
        print("Error:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def delete_transaction():
    try:
        transaction_id = int(input("Enter Transaction ID to delete: "))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM transactions WHERE id = %s",
            (transaction_id,)
        )

        if cursor.rowcount > 0:
            conn.commit()
            print("Transaction deleted successfully!")
        else:
            print("Transaction not found!")

    except ValueError:
        print("Enter a valid Transaction ID.")

    except Exception as e:
        print("Error:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def view_balance():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END),
                SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END)
            FROM transactions
        """)

        result = cursor.fetchone()

        total_income = result[0] or 0
        total_expenses = result[1] or 0
        balance = total_income - total_expenses

        print("\n========== FINANCIAL SUMMARY ==========")
        print(f"Total Income:    ₹{total_income:.2f}")
        print(f"Total Expenses:  ₹{total_expenses:.2f}")
        print("---------------------------------------")
        print(f"Current Balance: ₹{balance:.2f}")

    except Exception as e:
        print("Error:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def monthly_summary():
    try:
        year = int(input("Enter year (YYYY): "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("Invalid month! Enter a month between 1 and 12.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END),
            SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END)
        FROM transactions
        WHERE YEAR(transaction_date) = %s
        AND MONTH(transaction_date) = %s
        """

        cursor.execute(query, (year, month))
        result = cursor.fetchone()

        income = result[0] or 0
        expenses = result[1] or 0
        balance = income - expenses

        print("\n========== MONTHLY SUMMARY ==========")
        print("Month:", month, "/", year)
        print(f"Total Income:   ₹{income:.2f}")
        print(f"Total Expenses: ₹{expenses:.2f}")
        print("-------------------------------------")
        print(f"Monthly Balance: ₹{balance:.2f}")

    except ValueError:
        print("Please enter valid year and month.")

    except Exception as e:
        print("Error:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def menu():
    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Search Transaction")
        print("5. Update Transaction")
        print("6. Delete Transaction")
        print("7. View Balance")
        print("8. Monthly Summary")
        print("9. Exit")

        choice=input("\nEnter your choice")

        if choice=="1":
            add_income()

        elif choice=="2":
            add_expense()

        elif choice=="3":
            view_transactions()

        elif choice == "4":
            search_transaction()

        elif choice == "5":
            update_transaction()

        elif choice == "6":
            delete_transaction()

        elif choice == "7":
            view_balance()

        elif choice == "8":
            monthly_summary()

        elif choice == "9":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    create_database()
    menu()