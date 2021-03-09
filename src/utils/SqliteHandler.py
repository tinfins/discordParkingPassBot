'''
SqliteHandler
Performs functions for interaction with SQLite databases
'''
import sqlite3
from sqlite3 import Error
import logging.config
from urllib.request import pathname2url


class SqliteHandler:
    '''
    Handler for all SQL commands for sqlite database for parkingPassMngr discord bot
    '''
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_file = None
        self.conn = None
    
    def check_database_exists(self, db_path):
        '''
        Check if SQLite database exists
        :param db_path:String:path to db (src/db/{guild_id}.db)
        :return: True if exists, else False
        '''
        db_id = pathname2url(f'{db_path}')
        self.db_file = f"file:{db_id}?mode=rw"
        try:
            conn = sqlite3.connect(self.db_file, uri=True)
            print(f'Database {db_id} exists!')
            self.logger.info('Database %s exists!', db_id)
            conn.close()
            return True
        except Error as ex:
            print(ex)
            self.logger.error(ex)
            return False

    def create_database(self, db_path):
        '''
        Create SQLite database
        :param db_path:String:path to db (src/db/{guild_id}.db)
        :return: True if exists, else False
        '''
        db_id = pathname2url(f'{db_path}')
        self.db_file = f"file:{db_id}?mode=rwc"
        try:
            conn = sqlite3.connect(self.db_file, uri=True)
            print(f'SQLite3 version: {sqlite3.version}')
            print(f'Database created at {db_id}')
            self.logger.info('SQLite3 version: %s', sqlite3.version)
            self.logger.info('Database created at %s', db_id)
            self.close_connection(conn)
            return True
        except Error as ex:
            print(ex)
            self.logger.error(ex)
            return False
    
    def create_connection(self, db_path):
        '''
        Create connection to SQLite database
        :param db_path:String:path to db (src/db/{guild_id}.db)
        :return: Connection object, else None if error
        '''
        try:
            conn = sqlite3.connect(db_path, uri=True)
            return conn
        except Error as ex:
            print(ex)
            self.logger.error(ex)
            return None
    
    def close_connection(self, conn, cur=None):
        '''
        Close connection to SQLite database
        :param conn:SQLite connection object
        :return:True if closed, else False
        '''
        try:
            if cur:
                cur.close()
            conn.close()
            return True
        except Error as ex:
            print(ex)
            self.logger.error(ex)
            return False
    
    def execute_select(self, conn, sql, task=None):
        '''
        Execute select command with SQLite connection object
        :param conn: SQLite connection object
        :param sql: SQL statement to execute
        :param task: Parameters for SQL query
        :return:Cursor if success, else None
        '''
        self.conn = conn
        try:
            cur = self.conn.cursor()
            if task:
                cur.execute(sql, task)
            else:
                cur.execute(sql)
            return cur
        except Error as ex:
            print(ex)
            self.logger.error(ex)
            return None
    
    def execute_sql(self, conn, sql, task=None):
        '''
        Execute SQLite Insert, Update, and Drop statements
        :param conn: SQLite connection object
        :param sql: SQL statement to execute
        :param task: Parameters for SQL query
        :return:True if command executed, else False
        '''
        try:
            cur = conn.cursor()
            if task:
                cur.execute(sql, task)
                conn.commit()
            else:
                cur.execute(sql)
                conn.commit()
            return True
        except Error as ex:
            print(ex)
            self.logger.error(ex)
            return False
