import mysql.connector
from datetime import datetime

from mysql.connector import utils

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

    @staticmethod
    def isEmpty(input):
        if type(input) in [tuple, list, dict, str] and len(input) == 0:
            return True
        return False

    @staticmethod
    def isNotEmpty(input):
        return not Util.isEmpty(input)
    
    @staticmethod
    def isNone(input):
        """
        For convenience of None judgement
        """
        if input is None:
            return True
        elif input == "all":
            return True
        elif Util.isEmpty(input):
            return True
        else:
            return False
    
    @staticmethod
    def isNotNone(input):
        return not Util.isNone(input)

    @staticmethod
    def whereBuild(conditionDict: dict) -> str:
        """build where clause, subclauses with space in front

        Args:
            conditionDict (dict): must be in format {'column_name': {'left': xxx, 'eq': xxx, 'right': xxx}}, ignore if no

        Returns:
            str: constructed where clause
        """
        andclause = " AND"
        clause = " WHERE"
        if Util.isEmpty(conditionDict):
            return ""
        subclause = ""
        for colname in conditionDict.keys():
            col = conditionDict[colname]
            if 'eq' in col.keys():
                subclause = " `{}`={}".format(colname, Util.fit(col['eq']))
            else:
                subclause_left = ""
                subclause_right = ""
                if 'left' in col.keys():
                    subclause_left = " `{}`>={}".format(colname, Util.fit(col['left']))
                if 'right' in col.keys():
                    subclause_right = " `{}`<={}".format(colname, Util.fit(col['right']))
                if Util.isNotEmpty(subclause_left) and Util.isNotEmpty(subclause_right):
                    subclause = subclause_left + andclause + subclause_right
                elif not Util.isEmpty(subclause_left):
                    subclause = subclause_left
                elif not Util.isEmpty(subclause_right):
                    subclause = subclause_right
            if clause == " WHERE":
                clause += subclause
            else:
                clause = clause + andclause + subclause
        return clause
        
class ReturnStatus:
    """
    For easy of info transmit between front and back end
    """
    OK = 0
    DATABASE_ERROR = -1
    DATA_NOT_UNIQUE = -2
    class ACCOUNT_ERROR:
        AMOUNT_SHORT = -3
        AMOUNT_NOT_ZERO = -4
        ACCOUNT_NOT_MATCH_CUSTOMER = -5
    class LOGIN_ERROR:
        PWD_NOT_MATCH = -6

    @staticmethod
    def statusToNarration(status):
        """Get narration of status

        Args:
            status (int): status

        Returns:
            str: narration
        """
        if status == ReturnStatus.OK:
            return "OK"
        elif status == ReturnStatus.DATABASE_ERROR:
            return "Database Error! "
        elif status == ReturnStatus.DATA_NOT_UNIQUE:
            return "Data submitted is not unique! "
        elif status == ReturnStatus.ACCOUNT_ERROR.AMOUNT_SHORT:
            return "Account balance short! "
        elif status == ReturnStatus.ACCOUNT_ERROR.AMOUNT_NOT_ZERO:
            return "Account balance not zero! "
        elif status == ReturnStatus.ACCOUNT_ERROR.ACCOUNT_NOT_MATCH_CUSTOMER:
            return "Account id doesn't match customer id! "
        elif status == ReturnStatus.LOGIN_ERROR.PWD_NOT_MATCH:
            return "Password wrong! "

    @staticmethod
    def isAStatus(content):
        """Check whether it is content or status (status is int)

        Args:
            content ([type]): [description]

        Returns:
            [type]: [description]
        """
        if content is int:
            return True
        else:
            return False

class WeConnect:
    def __init__(self) -> None:
        # 0 Create database connection
        self.myconn = mysql.connector.connect(host="localhost", user="root", database="facerecognition")
        self.date = datetime.utcnow()
        self.now = datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")
        self.cursor = self.myconn.cursor(buffered=True)
        # buffered=True, to avoid error when running on jupiter notebook
        # without the statement, error will be raised when following functions called without part 0 being called again

    # 1 Display Login Information
    def display_login_info(self, customer_id: int):
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
            self.cursor.execute(sql)
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return self.cursor.fetchone()

    # 1.1 Search user by username
    def read_user_by_name(self, name: str):
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
            self.cursor.execute(sql)
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return self.cursor.fetchall()

    # 1.2 Create User
    def create_user(self, name: str, pwd: str) -> int:
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
            self.cursor.execute(unique_check_sql)
            result = self.cursor.fetchall()
            if result is None:
                return ReturnStatus.DATABASE_ERROR
            elif len(result) != 0:
                return ReturnStatus.DATA_NOT_UNIQUE
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        try:
            self.cursor.execute("SELECT MAX(customer_id) FROM Customer;")
            customer_id = self.cursor.fetchone()[0] + 1
            entry = (customer_id, name, pwd)
            entry = Util.fitArray(entry)
            sql = "INSERT INTO Customer VALUES ({}, {}, {})".format(*entry)
            self.cursor.execute(sql)
            self.myconn.commit()
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return ReturnStatus.OK


    # # 2 Customized Welcome Information
    # def set_welcome_msg(customer_id: int, new_msg: str) -> int:
    #     """
    #     Set the welcome message for a user

    #     Keyword Argument:
    #     customer_id -- int, the id of customer want to change the welcome message
    #     new_msg -- str, the new welcome message to set

    #     Return True if set success, False if fails
    #     """
    #     try:
    #         sql = "UPDATE Customer SET welcome_msg = '{}' WHERE customer_id = '{}';".format(new_msg, customer_id)
    #         self.cursor.execute(sql)
    #     except BaseException:
    #         return ReturnStatus.DATABASE_ERROR
    #     return ReturnStatus.OK

    # A user profile
    # A.1 Read User Profile
    def read_profile(self, customer_id: int):
        """
        :param customer_id:
        :return: tuple (name, gender, birthday, email, pic, welcome_msg, is_public)
        name: name of user
        gender: 0 M, 1 F, 2 Other
        birthday:
        email:
        pic: profile pic file path
        welcome_msg: welcome message
        is_public: whether profile is open to other users (tentative function). 0 no, 1 yes
        """
        try:
            sql = """SELECT name, gender, DATE_FORMAT(birthday, '%Y-%m-%d'), email, pic, welcome_msg, is_public
                    FROM Profile
                    WHERE customer_id = '{}';""".format(customer_id)
            self.cursor.execute(sql)
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return self.cursor.fetchone()

    # A.2 Update User Profile
    def update_profile(self, customer_id: int, name:str=None, gender:str=None, birthday:str=None, email:str=None, pic:str=None, welcome_msg:str=None, is_public:bool=None) -> int:
        """
        Args:
            customer_id:
            name: name to update
            gender: 0 M, 1 F, 2 Other
            birthday: in '%Y-%m-%d' format
            email:
            pic: file path
            welcome_msg: welcome message
            is_public: 0 no, 1 yes

        Returns: True on success, False on failure

        """
        original = self.read_profile(customer_id)
        if original is None:
            return False
        update = [name, gender, birthday, email, pic, welcome_msg, is_public]
        original = Util.updateArray(original, update)
        original = Util.fitArray(original)
        try:
            sql = """
            UPDATE Profile SET `name` = {}, `gender` = {}, `birthday` = {}, `email` = {}, `pic` = {}, `welcome_msg` = {}, `is_public` = {} WHERE (`profile_id` = {});
            """.format(*original, customer_id)
            self.cursor.execute(sql)
            self.myconn.commit()
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return ReturnStatus.OK


    # A.3 Update User Pic
    def update_profile_pic(self, customer_id: int, pic:str=None) -> int:
        """
        Args:
            customer_id:
            pic: file path

        Returns: True on success, False on failure

        """
        return self.update_profile(customer_id,
                            name=None, gender=None, birthday=None, email=None, pic=pic, welcome_msg=None, is_public=None)

    # A.4 Update Profile Publicness
    def update_profile_public(self, customer_id: int, is_public: int=None) -> int:
        """
        Args:
            customer_id:
            is_public: 0 no 1 yes

        Returns: True on success, False on failure

        """
        return self.update_profile(customer_id,
                            name=None, gender=None, birthday=None, email=None, pic=None, welcome_msg=None, is_public=is_public)

    # A.5 Create User Profile
    def create_profile(self, customer_id: int, name:str=None, gender:str=None, birthday:str=None, email:str=None, pic:str=None, welcome_msg:str=None, is_public:bool=None) -> int:
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
            self.cursor.execute("SELECT MAX(profile_id) FROM Profile;")
            profile_id = self.cursor.fetchone()[0] + 1
            entry = (profile_id, customer_id, name, gender, birthday, email, pic, welcome_msg, is_public)
            entry = Util.fitArray(entry)
            sql = "INSERT INTO Profile (`profile_id`, `customer_id`, `name`, `gender`, `birthday`, `email`, `pic`, `welcome_msg`, `is_public`) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {});".format(*entry)
            self.cursor.execute(sql)
            self.myconn.commit()
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return ReturnStatus.OK


    # 3 View Account Information
    def get_account_info(self, customer_id: int) -> list:
        sql = """SELECT type, currency, account_id, balance FROM Account WHERE customer_id = {};""".format(customer_id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # # 4 See Detail Transaction
    # def get_transaction(account_id: int) -> list:
    #     """[summary]

    #     Args:
    #         account_id (int): [description]

    #     Returns:
    #         list: [description]
    #     """
    #     self.cursor.execute("SELECT TIME_FORMAT(transaction_time, '%H:%i:%s'), DATE_FORMAT(transaction_date, '%Y-%m-%d'), amount FROM Transaction WHERE account_id = {};".format(account_id))
    #     return self.cursor.fetchall()

    # 5 Search Detail Transaction
    # Support Time Range Selection
    # Support Date Selection and Date Range Selection
    # Support Amount Selection
    def search_transaction(self, from_account_id: int=None, to_account_id: int=None, date_left: str=None, date_right: str=None, 
    time_left: str=None, time_right: str=None, amount_low: int=None, amount_high: int=None) -> list:
        """
        Search transactions with various conditions. 
        currently allow only either search from self or to self

        Args:
            from_account_id (int, optional): [description]. Defaults to None.
            to_account_id (int, optional): [description]. Defaults to None.
            date_left (str, optional): [description]. Defaults to None.
            date_right (str, optional): [description]. Defaults to None.
            time_left (str, optional): [description]. Defaults to None.
            time_right (str, optional): [description]. Defaults to None.
            amount_low (int, optional): [description]. Defaults to None.
            amount_high (int, optional): [description]. Defaults to None.

        Returns:
            list: [description]
        """

        # prep where build
        conditions = {}
        if Util.isNotNone(from_account_id):
            conditions['from_account_id'] = {'eq': from_account_id}
        if Util.isNotNone(to_account_id):
            conditions['to_account_id'] = {'eq': to_account_id}
        if Util.isNotNone(date_left) or Util.isNotNone(date_right):
            conditions['transaction_date'] = {}
            if Util.isNotNone(date_left):
                conditions['transaction_date']['left'] = date_left
            if Util.isNotNone(date_right):
                conditions['transaction_date']['right'] = date_right
        if Util.isNotNone(time_left) or Util.isNotNone(time_right):
            conditions['transaction_time'] = {}
            if Util.isNotNone(time_left):
                conditions['transaction_time']['left'] = time_left
            if Util.isNotNone(time_right):
                conditions['transaction_time']['right'] = time_right
        if Util.isNotNone(amount_low) or Util.isNotNone(amount_high):
            conditions['amount'] = {}
            if Util.isNotNone(amount_low):
                conditions['amount']['left'] = amount_low
            if Util.isNotNone(amount_high):
                conditions['amount']['right'] = amount_high
        
        whereclause = Util.whereBuild(conditions)
        
        sql = "SELECT TIME_FORMAT(transaction_time, '%H:%i:%s'), DATE_FORMAT(transaction_date, '%Y-%m-%d'), amount FROM Transaction" + whereclause + ";"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # Additional 1 Create New Account 

    def create_account(self, customer_id: int, type: str, currency: str) -> int:
        try:
            self.cursor.execute("SELECT MAX(account_id) FROM Account;")
            account_id = self.cursor.fetchone()[0] + 1
            sql = "INSERT INTO Account VALUES ({}, '{}', '{}', {}, 0)".format(customer_id, type, currency, account_id)
            self.cursor.execute(sql)
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return ReturnStatus.OK

    # Additional 2 Delete Account

    def delete_account(self, customer_id: int, account_id: int) -> int:
        self.cursor.execute("SELECT customer_id, balance FROM Account WHERE account_id = {}".format(account_id))
        db_customer_id, balance = self.cursor.fetchone()
        # Reject Deletion if account not belong to this user or balance is not 0
        if db_customer_id != customer_id:
            return ReturnStatus.ACCOUNT_ERROR.ACCOUNT_NOT_MATCH_CUSTOMER
        if balance != 0:
            return ReturnStatus.ACCOUNT_ERROR.AMOUNT_NOT_ZERO
        try:
            self.cursor.execute("DELETE FROM Account WHERE account_id = {}".format(account_id))
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return ReturnStatus.OK

    # Additional 2 Make Transaction
    # Return True if transaction are proceeded, False otherwise
    def make_transaction(self, from_account: int, to_account: int, amount: int) -> int:
        try:
            # Verify Correctness
            self.cursor.execute("SELECT balance FROM Account WHERE account_id = {}".format(from_account))
            from_balance = self.cursor.fetchone()[0]
            if from_balance < amount:
                return ReturnStatus.ACCOUNT_ERROR.AMOUNT_SHORT
            # Update Transaction Infos
            self.cursor.execute("SELECT MAX(account_id) FROM Account;")
            transaction_id = self.cursor.fetchone()[0] + 1
            entry = (transaction_id, from_account, to_account, amount)
            sql = "INSERT INTO Transaction VALUES ({}, {}, CURDATE(), NOW(), {});".format(from_account, -amount, to_account, amount)
            self.cursor.execute(sql)
            # Update Account Infos
            self.cursor.execute("UPDATE Account SET balance = {} WHERE account_id = {}".format(from_balance - amount, from_account))
            self.cursor.execute("SELECT balance FROM Account WHERE account_id = {}".format(to_account))
            to_balance = self.cursor.fetchone()[0]
            self.cursor.execute("UPDATE Account SET balance = {} WHERE account_id = {}".format(to_balance + amount, to_account))
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return ReturnStatus.OK

    # Additional 3 Password Login
    # Return customer_id
    def password_login(self, name: str, pwd: str) -> int:
        try:
            self.cursor.execute("SELECT pwd FROM Customer WHERE name = '{}'".format(name))
            db_pwd = self.cursor.fetchone()[0]
            if db_pwd != pwd:
                return ReturnStatus.LOGIN_ERROR.PWD_NOT_MATCH
            self.cursor.execute("SELECT customer_id FROM Customer WHERE name = '{}'".format(name))
            return self.cursor.fetchone()[0]
        except BaseException:
            return ReturnStatus.DATABASE_ERROR