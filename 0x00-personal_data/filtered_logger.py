#!/usr/bin/env python3
""" module for filter_datum function """
import re
from typing import List
import logging
import mysql.connector
import os


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """ returns the log message obfuscated """
    fields = "|".join(fields)
    return re.sub(r'(?P<field>{})=[^{}]*'.format(fields,
                  separator), r'\g<field>={}'.format(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initialize the class """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ formater function """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ returns a logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propergate = False
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streamhandler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database """
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", 'root')
    pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db = os.getenv("PERSONAL_DATA_DB_NAME")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")

    return mysql.connector.connect(host=host, user=user, password=pwd, db=db)


def main():
    """ retrieve all rows in the users table and
    display each row under a filtered format like this"""

    db = get_db()
    logger = get_logger()
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM users;")

        users = cursor.fetchall()
        for user in users:
            message = '; '.join(
                map(lambda x: "{}={}".format(x[0], x[1]), user.items())) + ';'
            rec_log = logging.LogRecord(
                "user_data", 20, None, None, message, None, None)
            logger.handle(rec_log)


if __name__ == "__main__":
    main()
