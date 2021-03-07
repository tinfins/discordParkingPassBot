#pylint:disable=C0103
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
        self.table_name = 'parkingPass'
    
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
            self.logger.info('Database %s exists!', db_id)
            conn.close()
            return True
        except Error as ex:
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
            self.logger.info('SQLite3 version: %s', sqlite3.version)
            self.logger.info('Database created at %s', db_id)
            self.close_connection(conn)
            return True
        except Error as ex:
            self.logger.error(ex)
            return False
    
    def create_connection(self, db_path):
        '''
        Create connection to SQLite database
        :param db_path:String:path to db (src/db/{guild_id}.db)
        :return: Connection object, else None if error
        '''
        #db_id = pathname2url(f'{db_path}')
        #self.db_file = f"file:{db_id}?mode=rw"
        try:
            conn = sqlite3.connect(db_path, uri=True)
            return conn
        except Error as ex:
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
        except Error as e:
            self.logger.error(e)
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
            c = conn.cursor()
            if task:
                c.execute(sql, task)
                conn.commit()
            else:
                c.execute(sql)
                conn.commit()
            return True
        except Error as e:
            self.logger.error(e)
            return False
    
    def table_exists_sql(self, conn):
        '''
        Check if table exists
        :param conn: Connection object
        :return:var:True if table exists, else False
        '''
        sql = f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{self.table_name}'"
        cur = self.execute_select(conn, sql)
        var = bool(cur.fetchone()[0] == 1)
        #self.close_connection(conn, cur)
        return var
    
    def create_table_sql(self, conn):
        '''
        Form statement to create table
        :param conn: Connection object
        :return:var:True if success, else False
        '''
        sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} (pass_id integer PRIMARY KEY, name text, date text, out int NOT NULL);"
        var = self.execute_sql(conn, sql)
        self.close_connection(conn)
        return var
    
    def add_pass(self, conn, pass_num, out_bool):
        '''
        Form parameterized statement to add pass to table
        :param conn: Connection object
        :param pass_num: Parking pass number
        :param out: Boolean: 1 checked out, 0 checked in
        :return:var:True if success, else False
        '''
        sql = f"INSERT INTO {self.table_name} (pass_id, name, date, out) VALUES (?, ?, ?, ?)"
        task = (pass_num, 'none', 'none', out_bool,)
        var = self.execute_sql(conn, sql, task)
        self.close_connection(conn)
        return var
    
    def del_pass(self, conn, pass_num):
        '''
        Delete pass from sqlite database
        :param conn: Connection object
        :param pass_num: Parking pass number
        :return:var:True if success, else False
        '''
        sql = f"DELETE FROM {self.table_name} WHERE pass_id=?"
        task = (pass_num,)
        var = self.execute_sql(conn, sql, task)
        self.close_connection(conn)
        return var
    
    def update_pass(self, conn, pass_num, name, date, out):
        '''
        Update status of parking pass (checked in/checked out)
        :param conn: Connection object
        :param pass_num: Parking pass number
        :param name: Name from ctx.author
        :param date: Date as String
        :param out: Boolean: 1 out, 0 in
        :return:var:True if success, else False
        '''
        sql = f"UPDATE {self.table_name} SET name = ?, date = ?, out = ? WHERE pass_id = ?"
        task = (name, date, out, pass_num,)
        var = self.execute_sql(conn, sql, task)
        self.close_connection(conn)
        return var
    
    def check_pass(self, conn, pass_num):
        '''
        Check if pass exists in database
        :param pass_num: parking pass id
        :return:List:Parking pass info as List
        '''
        sql = f"SELECT * FROM {self.table_name} WHERE pass_id = ?"
        task = (pass_num,)
        cur = self.execute_select(conn, sql, task)
        p_pass = []
        for row in cur:
            p_pass.append(row)
        self.close_connection(conn, cur)
        return p_pass
    
    # FIX THIS
    def check_out_flag(self, conn, guild_id, pass_num):
        sql = f"SELECT out FROM [{guild_id}] WHERE pass_id = ? and out == 0"
        task = (pass_num,)
        cur = self.execute_select(conn, sql, task)
        for row in cur:
            return bool(row == 0)
    
    def select_passes(self, conn):
        '''
        Select all rows in table
        :param conn: Connection object
        :return:Dict of passes
        '''
        sql = f"SELECT * FROM {self.table_name}"
        conn.row_factory = sqlite3.Row
        cur = self.execute_select(conn, sql)
        rows = cur.fetchall()
        passes = []
        for row in rows:
            d = dict(zip(row.keys(), row))
            passes.append(d)
        self.close_connection(conn, cur)
        return passes
    