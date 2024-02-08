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
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            message,
            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ returns a logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setL(logging.INFO)
    logger.propergate = False
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streamhandler)

    return logger


def get_db():
    """ returns a connector to the database """
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", 'root')
    pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db = os.getenv("PERSONAL_DATA_DB_NAME")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    print(user, pwd, db, host)

    return mysql.connector.connect(host=host, user=user, password=pwd, db=db)
