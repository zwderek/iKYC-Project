import mysql.connector
from datetime import datetime

class Util:
    """
    utils, should be cut to other files later
    """
    @staticmethod
    def fit(string):
        """
        This function makes an element fit for sql use
        """
        if type(string) is str:
            return "\'" + string + "\'"
        elif string is None:
            return 'NULL'
        else:
            return string

    @staticmethod
    def fitArray(original):
        """
        change an (array of) element(s) into formats suitable for feeding into sql string without forced quotation mark
        """
        tp = type(original)
        if tp is str:
            return Util.fit(original)
        elif tp is tuple:
            new = tuple()
            for el in original:
                el = Util.fit(el)
                new += (el, )
            return new
        elif tp is list:
            # should not be using
            new = list()
            for el in original:
                el = Util.fit(el)
                new.append(el)
            return new
        else:
            return original
    
    @staticmethod
    def updateArray(original: tuple, update):
        original = list(original)
        for elidx in range(len(update)):
            el = update[elidx]
            if el is not None:
                original[elidx] = el
        return tuple(original)

class ReturnStatus:
    """
    For easy of info transmit between front and back end
    """
    OK = 0
    DATABASE_ERROR = -1
    DATA_NOT_UNIQUE = -2

    @staticmethod
    def statusToNarration(status):
        if status == ReturnStatus.OK:
            return "OK"
        elif status == ReturnStatus.DATABASE_ERROR:
            return "Database Error! "
        elif status == ReturnStatus.DATA_NOT_UNIQUE:
            return "Data submitted is not unique! "

    @staticmethod
    def isAStatus(content):
        if content is int:
            return True
        else:
            return False

# 0 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", database="facerecognition")
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor(buffered=True)
# buffered=True, to avoid error when running on jupiter notebook
# without the statement, error will be raised when following functions called without part 0 being called again

# 1 Display Login Information
def display_login_info(customer_id: int):
    """
    Get the Login Information with Name, Last Login Time, Last Login Date, Welcome Message, in sequence

    Keyword Arguments:
    customer_id -- int, id of customer

    Return a Tuple (name, login_time, login_date, welcome_message), query by index. On failure, return None.
    """
    try:
        sql = """SELECT name, TIME_FORMAT(login_time, '%H:%i:%s'), 
        DATE_FORMAT(login_date, '%Y-%m-%d'), 
        welcome_msg
        FROM Customer c LEFT JOIN
        Login l ON l.customer_id = c.customer_id
        WHERE c.customer_id = '{}'
        ORDER BY l.login_date DESC, l.login_time DESC;""".format(customer_id)
        cursor.execute(sql)
    except BaseException:
        return ReturnStatus.DATABASE_ERROR
    return cursor.fetchone()

# 1.1 Search user by username
def read_user_by_name(name: str):
    """
    Search user by username (blur search)
    Args:
        name: username (nickname)
    Return:
        list of records matching name [(customer_id, name)]
    """
    try:
        sql = """
        SELECT customer_id, name
        FROM Customer
        WHERE name LIKE '%{}%';
        """.format(name)
        cursor.execute(sql)
    except BaseException:
        return ReturnStatus.DATABASE_ERROR
    return cursor.fetchall()

# 1.2 Create User
def create_user(name: str, welcome_msg: str, pwd: str) -> int:
    """
    Creates user
    Args:
        name: username
        welcome_msg: user set welcome message
        pwd: password
    Returns:
        True on success, False on failure
    """
    try:
        unique_check_sql = "SELECT name FROM Customer WHERE name='{}';".format(name)
        cursor.execute(unique_check_sql)
        result = cursor.fetchall()
        if result is None:
            return ReturnStatus.DATABASE_ERROR
        elif len(result) != 0:
            return ReturnStatus.DATA_NOT_UNIQUE
    except BaseException:
        return ReturnStatus.DATABASE_ERROR
    try:
        cursor.execute("SELECT MAX(customer_id) FROM Customer;")
        customer_id = cursor.fetchone()[0] + 1
        entry = (customer_id, name, welcome_msg, pwd)
        entry = Util.fitArray(entry)
        sql = "INSERT INTO Customer VALUES ({}, {}, {}, {})".format(*entry)
        cursor.execute(sql)
        myconn.commit()
    except BaseException:
        return ReturnStatus.DATABASE_ERROR
    return ReturnStatus.OK


# 2 Customized Welcome Information
def set_welcome_msg(customer_id: int, new_msg: str) -> int:
    """
    Set the welcome message for a user

    Keyword Argument:
    customer_id -- int, the id of customer want to change the welcome message
    new_msg -- str, the new welcome message to set

    Return True if set success, False if fails
    """
    try:
        sql = "UPDATE Customer SET welcome_msg = '{}' WHERE customer_id = '{}';".format(new_msg, customer_id)
        cursor.execute(sql)
    except BaseException:
        return ReturnStatus.DATABASE_ERROR
    return ReturnStatus.OK

# A user profile
# A.1 Read User Profile
def read_profile(customer_id: int):
    """
    :param customer_id:
    :return: tuple (name, gender, birthday, email, pic, is_public)
    name: name of user
    gender: 0 M, 1 F, 2 Other
    birthday:
    email:
    pic: profile pic file path
    is_public: whether profile is open to other users (tentative function). 0 no, 1 yes
    """
    try:
        sql = """SELECT name, gender, DATE_FORMAT(birthday, '%Y-%m-%d'), email, pic, is_public
                FROM Profile
                WHERE customer_id = '{}';""".format(customer_id)
        cursor.execute(sql)
    except BaseException:
        return ReturnStatus.DATABASE_ERROR
    return cursor.fetchone()

# A.2 Update User Profile
def update_profile(customer_id: int, name:str=None, gender:str=None, birthday:str=None, email:str=None, pic:str=None, is_public:bool=None) -> int:
    """
    Args:
        customer_id:
        name: name to update
        gender: 0 M, 1 F, 2 Other
        birthday: in '%Y-%m-%d' format
        email:
        pic: file path
        is_public: 0 no, 1 yes

    Returns: True on success, False on failure

    """
    original = read_profile(customer_id)
    if original is None:
        return False
    update = [name, gender, birthday, email, pic, is_public]
    original = Util.updateArray(original, update)
    original = Util.fitArray(original)
    try:
        sql = """
        UPDATE Profile SET `name` = {}, `gender` = {}, `birthday` = {}, `email` = {}, `pic` = {}, `is_public` = {} WHERE (`profile_id` = {});
        """.format(*original, customer_id)
        cursor.execute(sql)
        myconn.commit()
    except BaseException:
        return ReturnStatus.DATABASE_ERROR
    return ReturnStatus.OK


# A.3 Update User Pic
def update_profile_pic(customer_id: int, pic:str=None) -> int:
    """
    Args:
        customer_id:
        pic: file path

    Returns: True on success, False on failure

    """
    return update_profile(customer_id,
                          name=None, gender=None, birthday=None, email=None, pic=pic, is_public=None)

# A.4 Update Profile Publicness
def update_profile_public(customer_id: int, is_public: int=None) -> int:
    """
    Args:
        customer_id:
        is_public: 0 no 1 yes

    Returns: True on success, False on failure

    """
    return update_profile(customer_id,
                          name=None, gender=None, birthday=None, email=None, pic=None, is_public=is_public)

# A.5 Create User Profile
def create_profile(customer_id: int, name:str=None, gender:str=None, birthday:str=None, email:str=None, pic:str=None, is_public:bool=None) -> int:
    """
    Create user profile
    Args:
        customer_id:
        name: name to update
        gender: 0 M, 1 F, 2 Other
        birthday: in '%Y-%m-%d' format
        email:
        pic: file path
        is_public: 0 no, 1 yes

    Returns: True on success, False on failure
    """
    try:
        cursor.execute("SELECT MAX(profile_id) FROM Profile;")
        profile_id = cursor.fetchone()[0] + 1
        entry = (profile_id, customer_id, name, gender, birthday, email, pic, is_public)
        entry = Util.fitArray(entry)
        sql = "INSERT INTO Customer (`profile_id`, `customer_id`, `name`, `gender`, `birthday`, `email`, `pic`, `is_public`) VALUES ({}, {}, {}, {}, {}, {}, {}, {})".format(*entry)
        cursor.execute(sql)
        myconn.commit()
    except BaseException:
        return ReturnStatus.DATABASE_ERROR
    return ReturnStatus.OK



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

def create_account(customer_id: int, type: str, currency: str) -> int:
    try:
        cursor.execute("SELECT MAX(account_id) FROM Account;")
        account_id = cursor.fetchone()[0] + 1
        sql = "INSERT INTO Account VALUES ({}, '{}', '{}', {}, 0)".format(customer_id, type, currency, account_id)
        cursor.execute(sql)
    except BaseException:
        return ReturnStatus.DATABASE_ERROR
    return ReturnStatus.OK

# Additional 2 Delete Account

def delete_account(customer_id: int, account_id: int) -> int:
    cursor.execute("SELECT customer_id, balance FROM Account WHERE account_id = {}".format(account_id))
    db_customer_id, balance = cursor.fetchone()
    # Reject Deletion if account not belong to this user or balance is not 0
    if db_customer_id != customer_id or balance != 0:
        return False
    try:
        cursor.execute("DELETE FROM Account WHERE account_id = {}".format(account_id))
    except BaseException:
        return ReturnStatus.DATABASE_ERROR
    return ReturnStatus.OK

# Additional 2 Make Transaction
# Return True if transaction are proceeded, False otherwise
def make_transaction(from_account: int, to_account: int, amount: int) -> int:
    try:
        # Verify Correctness
        cursor.execute("SELECT balance FROM Account WHERE account_id = {}".format(from_account))
        from_balance = cursor.fetchone()[0]
        if from_balance < amount:
            return ReturnStatus.ACCOUNT_ERROR.AMOUNT_SHORT
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