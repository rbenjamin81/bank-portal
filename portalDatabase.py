import mysql.connector
from mysql.connector import Error


class Database():
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="banks_portal",
                 user='root',
                 password='new_password'):

        self.host       = host
        self.port       = port
        self.database   = database
        self.user       = user
        self.password   = password
        self.connection = None
        self.cursor     = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host         = self.host,
                port         = self.port,
                database     = self.database,
                user         = self.user,
                password     = self.password)
            
            if self.connection.is_connected():
                return
        except Error as e:
            print("Error while connecting to MySQL", e)


    def getAllAccounts(self):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            query = "select * from accounts"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def getAllTransactions(self):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            query = "SELECT * FROM Transactions"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records
       
    def deposit(self, accountID, amount):
         if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            args = [accountID, amount]
            result_args = self.cursor.callproc('deposit', args)
            self.connection.commit()
            return result_args
   

    def withdraw(self, accountID, amount):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            args = [accountID, amount]
            result_args = self.cursor.callproc('withdraw', args)
            self.connection.commit()
            return result_args
        
    def addAccount(self, ownerName, owner_ssn, balance, status):
       if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            query = "INSERT INTO accounts (ownerName, owner_ssn, balance, account_status) VALUES (%s, %s, %s, %s)"
            values = (ownerName, owner_ssn, balance, status)
            self.cursor.execute(query, values)
            self.connection.commit()
  
    def accountTransactions(self, accountID):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            args = [accountID]
            result_args = self.cursor.callproc('accountTransactions', args)
            return result_args
  
    def deleteAccount(self, accountID):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor()
            delete_account_query = "DELETE FROM accounts WHERE accountId = %s"
            delete_transactions_query = "DELETE FROM Transactions WHERE accountID = %s"
            self.cursor.execute(delete_transactions_query, (accountID,))
            self.cursor.execute(delete_account_query, (accountID,))
            self.connection.commit()
        
        
        
    
    
