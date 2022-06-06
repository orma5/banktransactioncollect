import apsw
import os


class sqliteHandler:

    def __init__(self, sqliteDBFile):

        if os.path.exists(sqliteDBFile):

            self._dbConnection = apsw.Connection(sqliteDBFile)
            self._cursor = self._dbConnection.cursor()

        else:
            raise Exception("Database: "+sqliteDBFile+" does not exists")

    def __del__(self):

        self._cursor.close()

    def getActiveAccount(self):

        self._cursor.execute("SELECT account_name,account_id \
                              FROM account WHERE active = 1;")

        accountData = self._cursor.fetchall()
        return accountData

    def getTransactionCount(self, account_name):

        queryString = """SELECT count(*) FROM [transaction]
        WHERE account_name = ?;"""

        valuesData = (account_name,)

        self._cursor.execute(queryString, valuesData)

        queryResult = self._cursor.fetchone()
        return queryResult[0]

    def insertTransactions(self, transactionList):

        queryString = """INSERT INTO [transaction]
        (transaction_id,booking_date,description,amount,period,year,month,account_name)
        VALUES(?,?,?,?,?,?,?,?); """

        self._cursor.execute("BEGIN TRANSACTION;")
        self._cursor.executemany(queryString, transactionList)
        self._cursor.execute("COMMIT;")

    def getTransactionsForAccount(self, account_name):

        queryString = """SELECT * from [transaction] WHERE account_name = ?;"""

        valuesData = (account_name,)

        self._cursor.execute(queryString, valuesData)

        queryResult = self._cursor.fetchall()

        return queryResult
