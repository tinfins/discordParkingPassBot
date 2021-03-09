import sqlite3
from src.utils.SqliteHandler import SqliteHandler


class DatabaseHelper:
    def __init__(self, table_name):
        self.sqliteH = SqliteHandler()
        self.table_name = table_name
        self.conn = None
         
    def table_exists_sql(self, conn):
        '''
        Check if table exists
        :param conn: Connection object
        :return:var:True if table exists, else False
        '''
        sql = f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{self.table_name}'"
        cur = self.sqliteH.execute_select(conn, sql)
        var = bool(cur.fetchone()[0] == 1)
        self.sqliteH.close_connection(conn, cur)
        return var
        
    def create_table_sql(self, conn):
        '''
        Form statement to create table
        :param conn: Connection object
        :return:var:True if success, else False
        '''
        sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} (pass_id integer PRIMARY KEY, name text, date text, out int NOT NULL);"
        var = self.sqliteH.execute_sql(conn, sql)
        self.sqliteH.close_connection(conn)
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
        task = (int(pass_num), 'none', 'none', int(out_bool),)
        var = self.sqliteH.execute_sql(conn, sql, task)
        self.sqliteH.close_connection(conn)
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
        var = self.sqliteH.execute_sql(conn, sql, task)
        self.sqliteH.close_connection(conn)
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
        var = self.sqliteH.execute_sql(conn, sql, task)
        self.sqliteH.close_connection(conn)
        return var
    
    def check_pass(self, conn, pass_num):
        '''
        Check if pass exists in database
        :param pass_num: parking pass id
        :return:List:Parking pass info as List
        '''
        sql = f"SELECT * FROM {self.table_name} WHERE pass_id = ?"
        task = (pass_num,)
        conn.row_factory = sqlite3.Row
        cur = self.sqliteH.execute_select(conn, sql, task)
        rows = cur.fetchall()
        passes = []
        for row in rows:
            d = dict(zip(row.keys(), row))
            passes.append(d)
        self.sqliteH.close_connection(conn, cur)
        return passes
    
    def check_out_flag(self, conn, pass_num):
        sql = f"SELECT out FROM {self.table_name} WHERE pass_id = ?"
        task = (int(pass_num),)
        cur = self.sqliteH.execute_select(conn, sql, task)
        for row in cur:
            print(row[0])
            return bool(row == 1)
    
    def select_passes(self, conn):
        '''
        Select all rows in table
        :param conn: Connection object
        :return:Dict of passes
        '''
        sql = f"SELECT * FROM {self.table_name}"
        conn.row_factory = sqlite3.Row
        cur = self.sqliteH.execute_select(conn, sql)
        rows = cur.fetchall()
        passes = []
        for row in rows:
            d = dict(zip(row.keys(), row))
            passes.append(d)
        self.sqliteH.close_connection(conn, cur)
        return passes
    
    def connection(self, db_path):
        return SqliteHandler().create_connection(db_path)
    
    def setup(self, guild):
        db_path = f'src/db/{guild}.db'
        sqliteH = SqliteHandler()
        db_exists = sqliteH.check_database_exists(db_path)
        if db_exists is False:
            sqliteH.create_database(db_path)
        table_exists = self.table_exists_sql(self.connection(db_path))
        if table_exists is False:
            self.create_table_sql(self.connection(db_path))
    