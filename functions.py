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
    def makeIdValid(id: int) -> int:
        if id is None:
            return 0
        else:
            return id

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
        elif input == "NULL":
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
    def isValidResult(input):
        return Util.isNotNone(input) and not ReturnStatus.isAStatus(input)

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
    Return statuses must be <= 0, or it will be confused with ids
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
        NAME_NOT_EXISTING = -7
    DATA_NOT_EXISTING = -8

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
        elif status == ReturnStatus.LOGIN_ERROR.NAME_NOT_EXISTING:
            return "Username not existing! "
        elif status == ReturnStatus.DATA_NOT_EXISTING:
            return "Data not existing! "

    @staticmethod
    def isAStatus(content):
        """Check whether it is content or status (status is int)

        Args:
            content ([type]): [description]

        Returns:
            [type]: [description]
        """
        if type(content) is int and content <= 0:
            return True
        else:
            return False
    
    @staticmethod
    def isError(content):
        return ReturnStatus.isAStatus(content) and content < 0

class WeConnect:
    def __init__(self) -> None:
        # 0 Create database connection
        self.myconn = mysql.connector.connect(host="localhost", user="root", password="tanlihui991228", database="face")
        self.date = datetime.utcnow()
        self.now = datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")
        self.cursor = self.myconn.cursor(buffered=True)
        # buffered=True, to avoid error when running on jupiter notebook
        # without the statement, error will be raised when following functions called without part 0 being called again

    # 1 Display Login Information
    def display_login_info(self, customer_id: int):
        """
        Get the Login Information: customer information and user profile

        Keyword Arguments:
        customer_id -- int, id of customer

        Return a dictionary 
        {"customer_and_login": (name, login_time, login_date), "profile": (name, gender, birthday, email, pic, welcome_msg, is_public)}. 
        On failure, return None.
        """
        try:
            customer_and_login = self.read_customer_and_login(customer_id=customer_id)
            profile = self.read_profile(customer_id=customer_id)
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return {"customer_and_login": customer_and_login, "profile": profile}

    # 1.0 read_customer_and_login
    def read_customer_and_login(self, customer_id: int):
        """
        Get the Login Information with Name, Last Login Time, Last Login Date, in sequence

        Keyword Arguments:
        customer_id -- int, id of customer

        Return a Tuple (name, login_time, login_date), query by index. On failure, return error status.
        """
        try:
            sql = """SELECT name, TIME_FORMAT(login_time, '%H:%i:%s'), 
            DATE_FORMAT(login_date, '%Y-%m-%d')
            FROM Customer c LEFT JOIN
            Login l ON l.customer_id = c.customer_id
            WHERE c.customer_id = '{}'
            ORDER BY l.login_date DESC, l.login_time DESC;""".format(customer_id)
            self.cursor.execute(sql)
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        results = self.cursor.fetchall()
        if Util.isNone(results):
            return ReturnStatus.DATA_NOT_EXISTING
        return results[0]
        # return self.cursor.fetchone()

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
            customer_id on success, error status on failure
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
            customer_id = Util.makeIdValid(self.cursor.fetchone()[0]) + 1
            entry = (customer_id, name, pwd)
            entry = Util.fitArray(entry)
            sql = "INSERT INTO Customer VALUES ({}, {}, {})".format(*entry)
            self.cursor.execute(sql)
            res = self._create_profile(customer_id)
            if res != ReturnStatus.OK:
                return res
            self.myconn.commit()
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return customer_id

    # B login history
    # B.1 history record
    def create_history(self, customer_id: int, login_date: str=None, login_time: str=None) -> int:
        """Create login history record

        Args:
            customer_id (int): 
            login_date (str, optional): login date. Defaults to None, then today.
            login_time (str, optional): login time. Defaults to None, then now.

        Returns:
            int: ReturnStatus
        """
        try:
            self.cursor.execute("SELECT MAX(login_id) FROM Login;")
            login_id = self.cursor.fetchone()[0] + 1
            date = Util.fit(login_date) if login_date else 'CURDATE()'
            time = Util.fit(login_time) if login_time else 'NOW()'
            entry = (login_id, customer_id, date, time)
            sql = "INSERT INTO Login VALUES ({}, {}, {}, {})".format(*entry)
            self.cursor.execute(sql)
            self.myconn.commit()
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return ReturnStatus.OK

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
        results = self.cursor.fetchall()
        if Util.isNone(results):
            return ReturnStatus.DATA_NOT_EXISTING
        return results[0]

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
            return ReturnStatus.DATA_NOT_EXISTING
        update = [name, gender, birthday, email, pic, welcome_msg, is_public]
        original = Util.updateArray(original, update)
        original = Util.fitArray(original)
        try:
            sql = """
            UPDATE Profile SET `name` = {}, `gender` = {}, `birthday` = {}, `email` = {}, `pic` = {}, `welcome_msg` = {}, `is_public` = {} WHERE (`customer_id` = {});
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
    # private method
    def _create_profile(self, customer_id: int, name:str=None, gender:str=None, birthday:str=None, email:str=None, pic:str=None, welcome_msg:str=None, is_public:bool=0) -> int:
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
            profile_id = Util.makeIdValid(self.cursor.fetchone()[0]) + 1
            entry = (profile_id, customer_id, name, gender, birthday, email, pic, welcome_msg, is_public)
            entry = Util.fitArray(entry)
            sql = "INSERT INTO Profile (`profile_id`, `customer_id`, `name`, `gender`, `birthday`, `email`, `pic`, `welcome_msg`, `is_public`) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {});".format(*entry)
            self.cursor.execute(sql)
            # self.myconn.commit()
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return ReturnStatus.OK


    # 3 View Account Information
    def get_account_info(self, customer_id: int) -> list:
        sql = """SELECT type, currency, account_id, balance FROM Account WHERE customer_id = {};""".format(customer_id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

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
            list: [(from_name, to_name, trans_time, trans_date, amount)]
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
        
        sql = """SELECT FC.name, TC.name, TIME_FORMAT(transaction_time, '%H:%i:%s'), DATE_FORMAT(transaction_date, '%Y-%m-%d'), amount
                FROM Transaction T left join
                Account FA on T.from_account_id = FA.account_id
                left join Account TA on T.to_account_id = TA.account_id
                left join Customer FC on FA.customer_id = FC.customer_id
                left join Customer TC on TA.customer_id = TC.customer_id
        """ + whereclause + ";"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # Additional 1 Create New Account 

    def create_account(self, customer_id: int, type: str, currency: str) -> int:
        """Create account

        Args:
            customer_id (int): [description]
            type (str): [Current, Saving, Borrowing]
            currency (str): [CYN, HKD, USD, ...]

        Returns:
            int: [success: account_id, failure: return status]
        """
        try:
            self.cursor.execute("SELECT MAX(account_id) FROM Account;")
            account_id = Util.makeIdValid(self.cursor.fetchone()[0]) + 1
            sql = "INSERT INTO Account VALUES ({}, '{}', '{}', {}, 0)".format(customer_id, type, currency, account_id)
            self.cursor.execute(sql)
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return account_id

    # Additional 2 Delete Account

    def delete_account(self, customer_id: int, account_id: int) -> int:
        """Delete account

        Args:
            customer_id (int): [description]
            account_id (int): [description]

        Returns:
            int: [return status]
        """
        self.cursor.execute("SELECT customer_id, balance FROM Account WHERE account_id = {}".format(account_id))
        results = self.cursor.fetchall()
        if Util.isNone(results):
            return ReturnStatus.DATA_NOT_EXISTING
        db_customer_id, balance = results[0]
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
        """Make transaction. This function should record a transaction, and make changes to the two accounts in concern

        Args:
            from_account (int): [id]
            to_account (int): [id]
            amount (int): [> 0]

        Returns:
            int: [return status]
        """
        try:
            # Verify Correctness
            self.cursor.execute("SELECT balance FROM Account WHERE account_id = {}".format(from_account))
            results = self.cursor.fetchall()
            if Util.isNone(results):
                return ReturnStatus.DATA_NOT_EXISTING
            from_balance = results[0][0]
            if from_balance < amount:
                return ReturnStatus.ACCOUNT_ERROR.AMOUNT_SHORT
            # Update Transaction Infos
            self.cursor.execute("SELECT MAX(transaction_id) FROM Transaction;")
            transaction_id = Util.makeIdValid(self.cursor.fetchone()[0]) + 1
            entry = (transaction_id, from_account, to_account, amount)
            sql = "INSERT INTO Transaction VALUES ({}, {}, {}, CURDATE(), NOW(), {});".format(*entry)
            self.cursor.execute(sql)
            # Update Account Infos
            self.cursor.execute("UPDATE Account SET balance = {} WHERE account_id = {}".format(from_balance - amount, from_account))
            self.cursor.execute("SELECT balance FROM Account WHERE account_id = {}".format(to_account))
            results = self.cursor.fetchall()
            if Util.isNone(results):
                return ReturnStatus.DATA_NOT_EXISTING
            to_balance = results[0][0]
            # to_balance = self.cursor.fetchone()[0]
            self.cursor.execute("UPDATE Account SET balance = {} WHERE account_id = {}".format(to_balance + amount, to_account))
            self.myconn.commit()
        except BaseException:
            return ReturnStatus.DATABASE_ERROR
        return ReturnStatus.OK

    # Additional 3 Password Login
    # Return customer_id
    def password_login(self, name: str, pwd: str) -> int:
        """Check whether password is correct or not

        Args:
            name (str): username
            pwd (str): password

        Returns:
            int: customer_id on success, error status on failure
        """
        try:
            self.cursor.execute("SELECT pwd FROM Customer WHERE name = '{}'".format(name))
            res = self.cursor.fetchone()
            if Util.isNone(res):
                return ReturnStatus.LOGIN_ERROR.NAME_NOT_EXISTING
            db_pwd = res[0]
            # db_pwd = self.cursor.fetchone()[0]
            if db_pwd != pwd:
                return ReturnStatus.LOGIN_ERROR.PWD_NOT_MATCH
            self.cursor.execute("SELECT customer_id FROM Customer WHERE name = '{}'".format(name))
            return self.cursor.fetchone()[0]
        except BaseException:
            return ReturnStatus.DATABASE_ERROR