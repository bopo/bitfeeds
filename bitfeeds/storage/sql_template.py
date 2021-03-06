#!/bin/python

from bitfeeds.storage.sql import SqlStorage
from bitfeeds.util import Logger

class SqlStorageTemplate(SqlStorage):
    """
    Sql storage template
    """
    def __init__(self):
        """
        Constructor
        """
        SqlStorage.__init__(self)

    def connect(self, **kwargs):
        """
        Connect
        """
        return True
        
    def execute(self, sql):
        """
        Execute the sql command
        :param sql: SQL command
        """
        Logger.info(self.__class__.__name__, "Execute command = %s" % sql)
        
    def commit(self):
        """
        Commit
        """    
        pass
        
    def fetchone(self):
        """
        Fetch one record
        :return Record
        """        
        return []

    def fetchall(self):
        """
        Fetch all records
        :return Record
        """        
        return []

