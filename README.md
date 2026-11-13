# 💰 Personal Expense Tracker

A Python and MySQL-based application designed to manage personal finances efficiently. It allows users to record income and expenses, track transactions, calculate balances, and generate monthly financial summaries.

## 🚀 Features

- **Add Income:** Record income with amount, category, description, and date.
- **Add Expense:** Track daily expenses.
- **View Transactions:** Display all recorded transactions.
- **Search Transactions:** Find transactions using their ID.
- **Update Transactions:** Modify existing transaction details.
- **Delete Transactions:** Remove unwanted records.
- **View Balance:** Calculate total income, total expenses, and current balance.
- **Monthly Summary:** Generate income and expense summaries for a selected month.
- **Input Validation:** Prevent invalid amounts and dates.

## 🛠️ Technologies Used

- Python 3
- MySQL
- MySQL Connector for Python
- VS Code

## 📁 Project Structure

```text
Personal-Expense-Tracker/
│
├── main.py
├── database.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/amrutha232006/Personal-Expense-Tracker
```

### 2. Navigate to the Project Folder

```bash
cd Personal-Expense-Tracker
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

- Start MySQL using XAMPP.
- Update the database credentials in `database.py` if necessary.
- The application automatically creates the `expense_tracker` database and `transactions` table.

### 5. Run the Application

```bash
python main.py
```

## 🗄️ Database Structure

**Database:** `expense_tracker`

**Table:** `transactions`

| Column | Data Type | Description |
|---|---|---|
| id | INT | Primary key |
| type | VARCHAR(20) | Income or Expense |
| amount | DECIMAL(10,2) | Transaction amount |
| category | VARCHAR(50) | Transaction category |
| description | VARCHAR(255) | Transaction details |
| transaction_date | DATE | Transaction date |

## 📚 Learning Outcomes

Through this project, I practiced:

- Python functions and modular programming
- Python and MySQL connectivity
- CRUD operations
- SQL queries and aggregate functions
- Exception handling
- Input validation
- Git and GitHub

## 🔮 Future Improvements

- Graphical User Interface (GUI)
- Expense visualization using charts
- Category-wise expense analysis
- Export monthly reports to CSV or PDF
- User login and authentication

## 👩‍💻 Author

Developed as a hands-on project to strengthen Python programming and database management skills.

**If you find this project useful, feel free to explore the repository!** ⭐