"""
I provide use methods to communicate with the database
"""

import os
import pwd
from storm.locals import create_database, Store


def getStore():
    """
    I return a store object
    """
    database = getDB()
    store = Store(database)
    return store


def getDB():
    """
    I return a connection to the database
    """
    db_uri = getURI() 
    db = create_database("postgres://jburns:teamSONICSHADOWamy@127.0.0.1/postgres")
    return db 


def getURI():
    """
    I return a URI to be used in a database connection
    """
    user = pwd.getpwuid(os.getuid()).pw_name
    return "psql -U {0} postgres".format(user)
