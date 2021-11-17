# iKYC-Project
An Intelligent Know Your Customer (iKYC) system with facial ID login function by COMP3278 Group 22

## How to use
Switch to folder directly containing this file as working directory
### Install Requirements
All requirements are listed in Requirements.txt, note that it's different from provided, with specific version provided, open the shell and type:
```bash
pip install -r requirements.txt
```

You might need to specify `pip3` for macOs
```bash
pip3 install -r requirements.txt
```
### Setup database
To setup database, please at least setup five table schema, they're include in `mytable.sql`.

Please open console, login in to mysql, create a new database `facerecognition`, and use `source mytable.sql` to create table

```MySQL
CREATE DATABASE facerecognition;

USE facerecognition;

SOURCE mytable.sql
```

#### Change MySQL Connector Username, Password, and Database
Go to /main_GUI/funcitons.py, at the top:
```Python
user = ""
password = ""
database = ""
```
Please change the user, password, database to the `username`, `password` you login to setup database and change `database` to the database you have created before. So it means you can create database name based on your preference.

#### Import Test Data (Optional)
After setup schema, you can use this system but need to sign up first as there's no user. To facilitate your usage, we provide some sample data in directory TestData:

```MySQL
SOURCE TestData/face_customer.sql;
SOURCE TestData/face_login.sql;
SOURCE TestData/face_profile.sql;
SOURCE TestData/face_account.sql;
SOURCE TestData/face_transaction.sql
```

After import test data, two test account are available:
|username|password|
|--|--|
|takagi|123|
|nishikata|123|
### Start the program
Entrance of program is `main.py` under folder `main_GUI`, so open the console and type:
```Python
python main_GUI/main.py
```

or `python3 main_GUI/main.py` for macOs users.

#### When you first entry the program
Though not requried, you're strongly recommended to register yourself, including username, password, and your face id!

Select `Sign Up`, choose yourself an username, which can not be used by other users before, select a password and confirm it by retyping, then click submit. If your username, password is valid, then camera will be invoked automatically to capture your face and train the face id model. Please wait a minute as it might takes a while for `opencv` to train.

#### After you login
You can start playing with this program.

## Funtions
1. When a customer login with his/her face ID, his/her information such as name, login time, login history, and customized welcome message will be presented in the GUI.
2. The customer can view his/her account information such as a list of accounts (e.g. saving, current, HKD, USD, etc.), account numbers, balances, etc.
3. The customer can click the account to see the detail transactions, and search the
transactions based on month, day, time and amount.
4. The transactions can be presented in the GUI.

## Additional Functions
1. User can sign up for new account, even with real-time recorded face id.
2. User can have profile more than simple welcome message, and can modify his/her profile and choose to publicate it to public
3. User can apply for new account by choosing type and currency
4. User can search transactions with a specific account, including cash inflow and cash outflow
5. User can delete their account if balance of account is 0.
6. User can make transactions with other accounts
