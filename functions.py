import mysql.connector
from datetime import datetime

# 0 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", database="facerecognition")
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

# 1 Display Login Information
def display_login_info(name: str) -> tuple:
    sql = """SELECT name, TIME_FORMAT(login_time, '%H:%i:%s'), 
    DATE_FORMAT(login_date, '%Y-%m-%d'), 
    welcome_msg FROM Customer
    WHERE name = '{}';""".format(name)
    cursor.execute(sql)
    return cursor.fetchone()

# 2 Customized Welcome Information
def set_welcome_msg(name: str, new_msg: str) -> bool:
    try:
        sql = "UPDATE Customer SET welcome_msg = '{}' WHERE name = '{}';".format(new_msg, name)
        cursor.execute(sql)
    except BaseException:
        return False
    return True

# 3 View Account Information
def get_account_info(customer_id: int) -> list:
    sql = """SELECT type, currency, account_id, balance FROM Account WHERE customer_id = {};""".format(customer_id);
    cursor.execute(sql)
    return cursor.fetchall()

# 4 See Detail Transaction
def get_transaction(account_id: int) -> list:
    cursor.execute("SELECT TIME_FORMAT(transaction_time, '%H:%i:%s'), DATE_FORMAT(transaction_date, '%Y-%m-%d'), amount FROM Transaction WHERE account_id = {};".format(account_id))
    return cursor.fetchall()

# 5 Search Detail Transaction
# Support Time Range Selection
# Support Date Selection and Date Range Selection
# Support Amount Selection
def search_transaction(account_id: int, date_left: str, date_right: str, 
time_left: str, time_right: str, amount_low: int, amount_high: int) -> list:
    sql = "SELECT TIME_FORMAT(transaction_time, '%H:%i:%s'), DATE_FORMAT(transaction_date, '%Y-%m-%d'), amount FROM Transaction WHERE transaction_date >= '{}' AND transaction_date <= '{}' AND transaction_time >= '{}' AND transaction_time <= '{}' AND amount >= {} AND amount <= {} AND account_id = {};".format(date_left, date_right, time_left, time_right, amount_low, amount_high, account_id)
    print(sql)
    cursor.execute(sql)
    return cursor.fetchall()

# Additional 1 Create New Account 

def create_account(customer_id: int, type: str, currency: str) -> bool:
    try:
        cursor.execute("SELECT MAX(account_id) FROM Account;")
        account_id = cursor.fetchone()[0] + 1
        sql = "INSERT INTO Account VALUES ({}, '{}', '{}', {}, 0)".format(customer_id, type, currency, account_id)
        cursor.execute(sql)
    except BaseException:
        return False
    return True

# Additional 2 Delete Account

def delete_account(customer_id: int, account_id: int) -> bool:
    cursor.execute("SELECT customer_id, balance FROM Account WHERE account_id = {}".format(account_id))
    db_customer_id, balance = cursor.fetchone()
    # Reject Deletion if account not belong to this user or balance is not 0
    if db_customer_id != customer_id or balance != 0:
        return False
    try:
        cursor.execute("DELETE FROM Account WHERE account_id = {}".format(account_id))
    except BaseException:
        return False
    return True

# Additional 2 Make Transaction
# Return True if transaction are proceed, False otherwise
def make_transaction(from_account: int, to_account: int, amount: int) -> bool:
    try:
        # Verify Correctness
        cursor.execute("SELECT balance FROM Account WHERE account_id = {}".format(from_account))
        from_balance = cursor.fetchone()[0]
        if from_balance < amount:
            return False
        # Update Transaction Infos
        sql = "INSERT INTO Transaction VALUES ({}, CURDATE(), NOW(), {}), ({}, CURDATE(), NOW(), {});".format(from_account, -amount, to_account, amount)
        cursor.execute(sql)
        # Update Account Infos
        cursor.execute("UPDATE Account SET balance = {} WHERE account_id = {}".format(from_balance - amount, from_account))
        cursor.execute("SELECT balance FROM Account WHERE account_id = {}".format(to_account))
        to_balance = cursor.fetchone()[0]
        cursor.execute("UPDATE Account SET balance = {} WHERE account_id = {}".format(to_balance + amount, to_account))
    except BaseException:
        return False
    return True

# Additional 3 Password Login
# Return customer_id
def password_login(name: str, pwd: str) -> int:
    try:
        cursor.execute("SELECT pwd FROM Customer WHERE name = '{}'".format(name))
        db_pwd = cursor.fetchone()[0]
        if db_pwd != pwd:
            return -1
        cursor.execute("SELECT customer_id FROM Customer WHERE name = '{}'".format(name))
        return cursor.fetchone()[0]
    except BaseException:
        return -1