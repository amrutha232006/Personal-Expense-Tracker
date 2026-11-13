import csv
from tkinter import filedialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import ttk, messagebox
from database import get_connection
from datetime import date

# ================= APPLICATION SETTINGS =================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Personal Expense Tracker")
app.geometry("1200x800")
app.minsize(1000, 700)


# ================= DASHBOARD HEADING =================

heading = ctk.CTkLabel(
    app,
    text="PERSONAL EXPENSE TRACKER",
    font=("Arial", 30, "bold")
)
heading.pack(pady=(20, 5))

welcome = ctk.CTkLabel(
    app,
    text="Manage your income and expenses easily!",
    font=("Arial", 16)
)
welcome.pack(pady=5)


# ================= DASHBOARD CARDS =================

dashboard = ctk.CTkFrame(app)
dashboard.pack(fill="x", padx=30, pady=20)

income_label = ctk.CTkLabel(
    dashboard,
    text="Total Income\n₹0.00",
    font=("Arial", 20, "bold"),
    text_color="green"
)
income_label.pack(side="left", expand=True, pady=25)

expense_label = ctk.CTkLabel(
    dashboard,
    text="Total Expenses\n₹0.00",
    font=("Arial", 20, "bold"),
    text_color="red"
)
expense_label.pack(side="left", expand=True, pady=25)

balance_label = ctk.CTkLabel(
    dashboard,
    text="Current Balance\n₹0.00",
    font=("Arial", 20, "bold")
)
balance_label.pack(side="left", expand=True, pady=25)


# ================= TRANSACTION TABLE =================

history_title = ctk.CTkLabel(
    app,
    text="Transaction History",
    font=("Arial", 23, "bold")
)
history_title.pack(pady=10)

columns = (
    "ID", "Type", "Amount",
    "Category", "Description", "Date"
)

table_frame = ctk.CTkFrame(app)
table_frame.pack(fill="both", expand=True, padx=30, pady=10)

transaction_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)

for column in columns:
    transaction_table.heading(column, text=column)
    transaction_table.column(
        column,
        width=150,
        anchor="center"
    )

transaction_table.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ================= REFRESH DASHBOARD =================

def refresh_dashboard():
    conn = None
    cursor = None

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

        income = float(result[0] or 0)
        expenses = float(result[1] or 0)
        balance = income - expenses

        income_label.configure(
            text=f"Total Income\n₹{income:.2f}"
        )

        expense_label.configure(
            text=f"Total Expenses\n₹{expenses:.2f}"
        )

        balance_label.configure(
            text=f"Current Balance\n₹{balance:.2f}"
        )

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ================= LOAD TRANSACTIONS =================

def load_transactions():
    conn = None
    cursor = None

    try:
        for item in transaction_table.get_children():
            transaction_table.delete(item)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM transactions
            ORDER BY transaction_date DESC, id DESC
        """)

        records = cursor.fetchall()

        for record in records:
            transaction_table.insert(
                "",
                "end",
                values=record
            )

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ================= ADD INCOME / EXPENSE =================

def add_transaction(transaction_type):

    window = ctk.CTkToplevel(app)
    window.title("Add " + transaction_type)
    window.geometry("400x480")
    window.grab_set()

    ctk.CTkLabel(
        window,
        text="Add " + transaction_type,
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    amount_entry = ctk.CTkEntry(
        window,
        placeholder_text="Amount"
    )
    amount_entry.pack(pady=10)

    category_entry = ctk.CTkEntry(
        window,
        placeholder_text="Category"
    )
    category_entry.pack(pady=10)

    description_entry = ctk.CTkEntry(
        window,
        placeholder_text="Description"
    )
    description_entry.pack(pady=10)

    date_entry = ctk.CTkEntry(
        window,
        placeholder_text="Date (YYYY-MM-DD)"
    )
    date_entry.pack(pady=10)

    def save_transaction():
        conn = None
        cursor = None

        try:
            amount = float(amount_entry.get())

            if amount <= 0:
                messagebox.showerror(
                    "Invalid Amount",
                    "Amount must be greater than zero!"
                )
                return

            category = category_entry.get().strip()
            description = description_entry.get().strip()
            transaction_date = date_entry.get().strip()

            if not category or not transaction_date:
                messagebox.showerror(
                    "Missing Details",
                    "Please enter category and date!"
                )
                return

            date.fromisoformat(transaction_date)

            conn = get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO transactions
                (type, amount, category, description, transaction_date)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                transaction_type,
                amount,
                category,
                description,
                transaction_date
            )

            cursor.execute(query, values)
            conn.commit()

            messagebox.showinfo(
                "Success",
                transaction_type + " added successfully!"
            )

            window.destroy()
            refresh_dashboard()
            load_transactions()

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid amount and date (YYYY-MM-DD)."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    ctk.CTkButton(
        window,
        text="Save Transaction",
        command=save_transaction
    ).pack(pady=20)


# ================= SEARCH TRANSACTIONS =================

def search_transactions():

    keyword = search_entry.get().strip()

    conn = None
    cursor = None

    try:
        for item in transaction_table.get_children():
            transaction_table.delete(item)

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT * FROM transactions
            WHERE category LIKE %s
            OR description LIKE %s
            ORDER BY transaction_date DESC
        """

        search_value = f"%{keyword}%"

        cursor.execute(
            query,
            (search_value, search_value)
        )

        records = cursor.fetchall()

        for record in records:
            transaction_table.insert(
                "",
                "end",
                values=record
            )

        if not records:
            messagebox.showinfo(
                "Search",
                "No matching transactions found!"
            )

    except Exception as e:
        messagebox.showerror("Search Error", str(e))

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ================= EDIT TRANSACTION =================

def edit_transaction():

    selected = transaction_table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Transaction",
            "Please select a transaction to edit!"
        )
        return

    record = transaction_table.item(
        selected[0], "values"
    )

    window = ctk.CTkToplevel(app)
    window.title("Edit Transaction")
    window.geometry("400x500")
    window.grab_set()

    ctk.CTkLabel(
        window,
        text="Edit Transaction",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    type_entry = ctk.CTkOptionMenu(
        window,
        values=["Income", "Expense"]
    )
    type_entry.set(record[1])
    type_entry.pack(pady=10)

    amount_entry = ctk.CTkEntry(
        window,
        placeholder_text="Amount"
    )
    amount_entry.insert(0, str(record[2]))
    amount_entry.pack(pady=10)

    category_entry = ctk.CTkEntry(
        window,
        placeholder_text="Category"
    )
    category_entry.insert(0, record[3])
    category_entry.pack(pady=10)

    description_entry = ctk.CTkEntry(
        window,
        placeholder_text="Description"
    )
    description_entry.insert(0, record[4])
    description_entry.pack(pady=10)

    date_entry = ctk.CTkEntry(
        window,
        placeholder_text="Date (YYYY-MM-DD)"
    )
    date_entry.insert(0, str(record[5]))
    date_entry.pack(pady=10)

    def save_changes():
        conn = None
        cursor = None

        try:
            amount = float(amount_entry.get())
            transaction_type = type_entry.get()
            category = category_entry.get().strip()
            description = description_entry.get().strip()
            transaction_date = date_entry.get().strip()

            if amount <= 0 or not category:
                messagebox.showerror(
                    "Invalid Input",
                    "Enter a positive amount and category."
                )
                return

            date.fromisoformat(transaction_date)

            conn = get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE transactions
                SET type=%s, amount=%s, category=%s,
                    description=%s, transaction_date=%s
                WHERE id=%s
            """

            values = (
                transaction_type,
                amount,
                category,
                description,
                transaction_date,
                record[0]
            )

            cursor.execute(query, values)
            conn.commit()

            messagebox.showinfo(
                "Success",
                "Transaction updated successfully!"
            )

            window.destroy()
            refresh_dashboard()
            load_transactions()

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Check the amount and date format."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    ctk.CTkButton(
        window,
        text="Save Changes",
        command=save_changes
    ).pack(pady=20)


# ================= DELETE TRANSACTION =================

def delete_transaction():

    selected = transaction_table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Transaction",
            "Please select a transaction to delete!"
        )
        return

    record = transaction_table.item(
        selected[0], "values"
    )

    transaction_id = record[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete transaction ID {transaction_id}?"
    )

    if not confirm:
        return

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM transactions WHERE id = %s",
            (transaction_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Transaction deleted successfully!"
        )

        refresh_dashboard()
        load_transactions()

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def show_analytics():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Expense category data
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE type = 'Expense'
            GROUP BY category
        """)

        category_data = cursor.fetchall()

        # Monthly income and expense data
        cursor.execute("""
            SELECT
                DATE_FORMAT(transaction_date, '%Y-%m'),
                SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END),
                SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END)
            FROM transactions
            GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
            ORDER BY DATE_FORMAT(transaction_date, '%Y-%m')
        """)

        monthly_data = cursor.fetchall()

    except Exception as e:
        messagebox.showerror("Analytics Error", str(e))
        return

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    # Analytics window
    analytics_window = ctk.CTkToplevel(app)
    analytics_window.title("Financial Analytics")
    analytics_window.geometry("1100x650")

    ctk.CTkLabel(
        analytics_window,
        text="Financial Analytics",
        font=("Arial", 26, "bold")
    ).pack(pady=15)

    # Create charts
    figure = Figure(figsize=(11, 5), dpi=100)

    ax1 = figure.add_subplot(121)
    ax2 = figure.add_subplot(122)

    # Pie chart
    if category_data:
        categories = [row[0] for row in category_data]
        amounts = [float(row[1]) for row in category_data]

        ax1.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=90
        )

        ax1.set_title("Expenses by Category")

    else:
        ax1.text(
            0.5, 0.5,
            "No expense data available",
            ha="center",
            va="center"
        )
        ax1.set_title("Expenses by Category")

    # Monthly bar chart
    if monthly_data:
        months = [row[0] for row in monthly_data]
        income = [float(row[1] or 0) for row in monthly_data]
        expenses = [float(row[2] or 0) for row in monthly_data]

        x = list(range(len(months)))
        width = 0.35

        ax2.bar(
            [i - width / 2 for i in x],
            income,
            width,
            label="Income"
        )

        ax2.bar(
            [i + width / 2 for i in x],
            expenses,
            width,
            label="Expenses"
        )

        ax2.set_xticks(x)
        ax2.set_xticklabels(months, rotation=45)
        ax2.set_title("Monthly Income vs Expenses")
        ax2.set_ylabel("Amount (₹)")
        ax2.legend()

    else:
        ax2.text(
            0.5, 0.5,
            "No transaction data available",
            ha="center",
            va="center"
        )
        ax2.set_title("Monthly Income vs Expenses")

    figure.tight_layout()

    # Display charts inside Tkinter
    canvas = FigureCanvasTkAgg(
        figure,
        master=analytics_window
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    def close_analytics():
        plt.close(figure)
        analytics_window.destroy()

    analytics_window.protocol(
        "WM_DELETE_WINDOW",
        close_analytics
    )


def export_transactions():
    conn = None
    cursor = None

    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Transactions"
        )

        if not file_path:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, type, amount, category,
                   description, transaction_date
            FROM transactions
            ORDER BY transaction_date DESC
        """)

        records = cursor.fetchall()

        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            writer.writerow([
                "ID", "Type", "Amount",
                "Category", "Description", "Date"
            ])

            writer.writerows(records)

        messagebox.showinfo(
            "Export Successful",
            f"Transactions exported successfully!\n{file_path}"
        )

    except Exception as e:
        messagebox.showerror("Export Error", str(e))

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def monthly_report():
    report_window = ctk.CTkToplevel(app)
    report_window.title("Monthly Spending Report")
    report_window.geometry("750x600")
    report_window.grab_set()

    ctk.CTkLabel(
        report_window,
        text="Monthly Spending Report",
        font=("Arial", 25, "bold")
    ).pack(pady=20)

    input_frame = ctk.CTkFrame(report_window)
    input_frame.pack(pady=10)

    month_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="Month (1-12)",
        width=130
    )
    month_entry.pack(side="left", padx=10)

    year_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="Year (YYYY)",
        width=130
    )
    year_entry.pack(side="left", padx=10)

    result_label = ctk.CTkLabel(
        report_window,
        text="Enter month and year to generate report.",
        font=("Arial", 16)
    )
    result_label.pack(pady=15)

    chart_frame = ctk.CTkFrame(report_window)
    chart_frame.pack(fill="both", expand=True, padx=15, pady=15)

    def generate_report():
        conn = None
        cursor = None

        try:
            month = int(month_entry.get())
            year = int(year_entry.get())

            if not 1 <= month <= 12 or not 1900 <= year <= 2100:
                messagebox.showerror(
                    "Invalid Input",
                    "Enter a valid month and year."
                )
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END),
                    SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END)
                FROM transactions
                WHERE YEAR(transaction_date) = %s
                AND MONTH(transaction_date) = %s
            """, (year, month))

            totals = cursor.fetchone()

            income = float(totals[0] or 0)
            expenses = float(totals[1] or 0)
            balance = income - expenses

            cursor.execute("""
                SELECT category, SUM(amount)
                FROM transactions
                WHERE type = 'Expense'
                AND YEAR(transaction_date) = %s
                AND MONTH(transaction_date) = %s
                GROUP BY category
                ORDER BY SUM(amount) DESC
            """, (year, month))

            categories = cursor.fetchall()

            result_label.configure(
                text=(
                    f"Income: ₹{income:.2f}    "
                    f"Expenses: ₹{expenses:.2f}    "
                    f"Balance: ₹{balance:.2f}"
                )
            )

            # Remove previous chart
            for widget in chart_frame.winfo_children():
                widget.destroy()

            figure = Figure(figsize=(7, 4), dpi=100)
            ax = figure.add_subplot(111)

            if categories:
                names = [row[0] for row in categories]
                amounts = [float(row[1]) for row in categories]

                ax.pie(
                    amounts,
                    labels=names,
                    autopct="%1.1f%%",
                    startangle=90
                )

                ax.set_title(
                    f"Expense Categories - {month}/{year}"
                )
            else:
                ax.text(
                    0.5, 0.5,
                    "No expenses recorded this month",
                    ha="center",
                    va="center"
                )

            figure.tight_layout()

            canvas = FigureCanvasTkAgg(
                figure,
                master=chart_frame
            )

            canvas.draw()
            canvas.get_tk_widget().pack(
                fill="both",
                expand=True
            )

            # Keep references alive
            report_window.chart_figure = figure
            report_window.chart_canvas = canvas

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid month and year."
            )

        except Exception as e:
            messagebox.showerror("Report Error", str(e))

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    ctk.CTkButton(
        report_window,
        text="Generate Report",
        command=generate_report
    ).pack(pady=15)

# ================= BUTTONS =================

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

ctk.CTkButton(
    button_frame,
    text="Add Income",
    width=150,
    command=lambda: add_transaction("Income")
).pack(side="left", padx=10)

ctk.CTkButton(
    button_frame,
    text="Add Expense",
    width=150,
    command=lambda: add_transaction("Expense")
).pack(side="left", padx=10)

ctk.CTkButton(
    button_frame,
    text="Refresh Dashboard",
    width=150,
    command=refresh_dashboard
).pack(side="left", padx=10)

ctk.CTkButton(
    button_frame,
    text="View Analytics",
    width=150,
    command=show_analytics
).pack(side="left", padx=10)


# ================= SEARCH BAR =================

search_frame = ctk.CTkFrame(app)
search_frame.pack(fill="x", padx=30, pady=10)

search_entry = ctk.CTkEntry(
    search_frame,
    placeholder_text="Search by category or description...",
    width=350
)
search_entry.pack(side="left", padx=10, pady=10)

ctk.CTkButton(
    search_frame,
    text="Search",
    command=search_transactions
).pack(side="left", padx=5)

ctk.CTkButton(
    search_frame,
    text="Show All",
    command=load_transactions
).pack(side="left", padx=5)

ctk.CTkButton(
    search_frame,
    text="Refresh Transactions",
    command=load_transactions
).pack(side="left", padx=5)


# ================= EDIT AND DELETE BUTTONS =================

action_frame = ctk.CTkFrame(app)
action_frame.pack(pady=10)

ctk.CTkButton(
    action_frame,
    text="Edit Selected",
    width=160,
    command=edit_transaction
).pack(side="left", padx=10)

ctk.CTkButton(
    action_frame,
    text="Delete Selected",
    width=160,
    fg_color="#C0392B",
    hover_color="#922B21",
    command=delete_transaction
).pack(side="left", padx=10)

ctk.CTkButton(
    action_frame,
    text="Export CSV",
    width=160,
    fg_color="#16803C",
    hover_color="#11632E",
    command=export_transactions
).pack(side="left", padx=10)

ctk.CTkButton(
    action_frame,
    text="Monthly Report",
    width=160,
    command=monthly_report
).pack(side="left", padx=10)

# ================= START APPLICATION =================

refresh_dashboard()
load_transactions()

app.mainloop()
