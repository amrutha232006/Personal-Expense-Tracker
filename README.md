# 💰 Personal Expense Tracker

A desktop-based Personal Expense Tracker developed using **Python, CustomTkinter, and MySQL**. This application helps users manage their personal finances by tracking income, expenses, monitoring balances, and generating monthly financial reports.

The application features a modern graphical user interface (GUI), interactive charts, and CSV export functionality.

## 🚀 Features

### 📊 Dashboard
- View total income.
- View total expenses.
- Calculate current balance.
- Refresh financial information.

### 💵 Transaction Management
- Add income and expenses.
- View all transactions.
- Search transactions by category or description.
- Edit existing transactions.
- Delete transactions.

### 📈 Financial Analytics
- Visualize expenses by category using pie charts.
- Compare monthly income and expenses using bar charts.
- Generate monthly financial summaries.
- View category-wise spending analysis.

### 📁 Data Export
- Export transaction history to CSV.
- Open exported records using Microsoft Excel or other spreadsheet applications.

### 🛡️ Input Validation
- Validate transaction amounts.
- Validate date formats.
- Handle invalid inputs and database errors.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| CustomTkinter | Modern desktop GUI |
| Tkinter | GUI components |
| MySQL | Database management |
| MySQL Connector | Database connectivity |
| Matplotlib | Charts and visual analytics |
| CSV | Export transaction records |

## 📂 Project Structure

```text
Personal-Expense-Tracker/
│
├── main.py
├── database.py
├── gui.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    ├── dashboard.png
    ├── transactions.png
    ├── analytics.png
    └── monthly-report.png
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
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

- Install and start XAMPP.
- Start the MySQL service.
- Configure your MySQL credentials in `database.py`.
- The application uses the `expense_tracker` database and `transactions` table.

### 5. Run the Application

```bash
python gui.py
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
| description | VARCHAR(255) | Transaction description |
| transaction_date | DATE | Transaction date |

## 📸 Application Screenshots

Add your application screenshots to the `screenshots` folder and display them here.

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Transaction History

![Transaction History](screenshots/transactions.png)

### Financial Analytics

![Financial Analytics](screenshots/analytics.png)

### Monthly Report

![Monthly Report](screenshots/monthly-report.png)

## 📚 Learning Outcomes

Through this project, I gained practical experience in:

- Python programming and modular development.
- Building desktop applications using CustomTkinter.
- Connecting Python applications with MySQL.
- Implementing CRUD operations.
- Writing SQL queries and aggregate functions.
- Creating charts using Matplotlib.
- Exporting data using CSV.
- Exception handling and input validation.
- Managing projects using Git and GitHub.

## 🔮 Future Enhancements

- User registration and login authentication.
- Password protection and individual user accounts.
- Budget planning and spending limits.
- PDF report generation.
- Advanced financial analytics.
- Improved dashboard customization.

## 👩‍💻 Author

Developed as a hands-on project to improve my Python programming, database management, and desktop application development skills.

**If you find this project useful, feel free to explore the repository and give it a ⭐!**