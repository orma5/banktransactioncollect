import os
import logging
from dotenv import load_dotenv
from api import nordigen
# from db import sqlite
from db import mariadb


def main():

    # LOAD ENV CONFIG

    load_dotenv()

    SID = os.getenv("NORDIGEN_SECRET_ID")
    SKEY = os.getenv("NORDIGEN_SECRET_KEY")
    # DB_FILE = os.getenv("BANK_TRANSACTION_SQLITE_DB")
    LOG_PATH = os.getenv("BANK_TRANSACTION_LOG_PATH")
    DB_USER = os.getenv("MARIADB_USER")
    DB_PASS = os.getenv("MARIADB_PASS")
    DB_HOST = os.getenv("MARIADB_HOST")
    DB_PORT = os.getenv("MARIADB_PORT")
    DB_NAME = os.getenv("MARIADB_DB")

    # INIT lOGGING

    logging.basicConfig(filename=LOG_PATH,
                        level=logging.INFO, format='%(asctime)s %(message)s')

    logging.info("<< Starting bank transaction collect >>")

    # INITIALIZE NORDIGEN SESSION

    logging.info("Initializing Norigen Session")
    nc = nordigen.NordigenClient(SID, SKEY)

    logging.info("Generaing Token")
    try:
        nc.generate_token()
        logging.info("Token generated successfully")
    except Exception as e:
        logging.error(e)

    # INITIALIZE DB
    logging.info("Loading database")
    db = mariadb.mariadbHandler(DB_USER,
                                DB_PASS,
                                DB_HOST,
                                int(DB_PORT),
                                DB_NAME)
    logging.info("Database loaded")

    # GET ACCOUNTS IDs
    logging.info("Fetching active accounts to process")
    bankAccounts = db.getActiveAccount()

    # GET TRANSACTIONS FOR ACCOUNTS
    for x in bankAccounts:

        account_name = x[0]
        account_id = x[1]

        logging.info("Processing account: \
         "+account_name+" with id:"+account_id)
        try:
            transactions = nc.getAllTransactionsForAccount(account_id)
            logging.info("Received account transactions, will now update db")

        except Exception as e:
            logging.error(e)

        transactionRecords = db.getTransactionCount(account_name)

        insertBatch = []

        for y in transactions:

            bookingDate = y["bookingDate"]
            amount = y["transactionAmount"]["amount"]
            transactionID = y["transactionId"]

            if "remittanceInformationUnstructuredArray" in y:
                description = y["remittanceInformationUnstructuredArray"][0]
            elif "creditorName" in y:
                description = y["creditorName"]
            elif "remittanceInformationUnstructured" in y:
                description = y["remittanceInformationUnstructured"]
            elif "additionalInformation" in y:
                description = y["additionalInformation"]
            else:
                description = y["proprietaryBankTransactionCode"]

            period = bookingDate[0:7]
            year = bookingDate[0:4]
            month = bookingDate[5:7]

            valuesData = [transactionID,
                          bookingDate,
                          description,
                          amount,
                          period,
                          year,
                          month,
                          account_name]
            insertBatch.append(valuesData)

        # INSERT NEW RECORDS IN DB
        db.insertTransactions(insertBatch)

        delta = db.getTransactionCount(account_name) - transactionRecords
        logging.info("Inserted "+str(delta)+" for account: "+account_name)
    logging.info("<< Bank transaction collect complete >>")


if __name__ == "__main__":
    main()
