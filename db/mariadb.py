import mariadb
import sys


class mariadbHandler:

    def __init__(self, dbUser, dbPassword, dbHost, dbPort, db):

        try:
            self._conn = mariadb.connect(
                user=dbUser,
                password=dbPassword,
                host=dbHost,
                port=dbPort,
                database=db
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        self._cursor = self._conn.cursor()

    def getActiveAccount(self):

        self._cursor.execute("SELECT account_name,account_id \
                              FROM account WHERE active = 1;")

        accountData = self._cursor.fetchall()
        return accountData

    def getTransactionCount(self, account_name):

        queryString = """SELECT count(*) FROM transaction
        WHERE account_name = ?;"""

        valuesData = (account_name,)

        self._cursor.execute(queryString, valuesData)

        queryResult = self._cursor.fetchone()
        return queryResult[0]

    def insertTransactions(self, transactionList):
        print(transactionList)
        transactionTupleList = list(map(tuple, transactionList))
        print(transactionTupleList)
        queryString = """INSERT IGNORE INTO transaction
        (transaction_id,booking_date,description,amount,period,year,month,account_name)
        VALUES(?,?,?,?,?,?,?,?); """

        self._cursor.executemany(queryString, transactionTupleList)
        self._conn.commit()

    def getTransactionsForAccount(self, account_name):

        queryString = """SELECT * from transaction WHERE account_name = ?;"""

        valuesData = (account_name,)

        self._cursor.execute(queryString, valuesData)

        queryResult = self._cursor.fetchall()

        return queryResult
