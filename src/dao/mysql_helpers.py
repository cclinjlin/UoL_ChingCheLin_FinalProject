from logs import LOGGER
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PWD, MYSQL_DB
import pymysql
import sys
sys.path.append("..")


class MySQLHelper():

    def __init__(self):
        # create connection
        self.conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, port=MYSQL_PORT, password=MYSQL_PWD,
                                    database=MYSQL_DB,
                                    local_infile=True)
        self.cursor = self.conn.cursor()

    def test_connection(self):
        try:
            self.conn.ping()
        except Exception:
            self.conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, port=MYSQL_PORT, password=MYSQL_PWD,
                                        database=MYSQL_DB, local_infile=True)
            self.cursor = self.conn.cursor()

    def insert_new_am(self, CompanyID, CompanyName, WebSite, CompanyDescription, DefaultAddress, Interests, Products, Projects, mid):
        self.test_connection()
        sql = f"INSERT IGNORE INTO am(CompanyID, CompanyName, WebSite, CompanyDescription, DefaultAddress, Interests, Products, Projects, mid )\
            VALUES ({CompanyID}, '{CompanyName}', \"{WebSite}\", \"{CompanyDescription}\", \"{DefaultAddress}\", '{Interests}', '{Products}', '{Projects}', {mid})"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            raise e
    
    def insert_new_am_2(self, CompanyName, WebSite, CompanyDescription, DefaultAddress, Interests, Products, Projects):
        self.test_connection()
        sql = f"INSERT IGNORE INTO am( CompanyName, WebSite, CompanyDescription, DefaultAddress, Interests, Products, Projects )\
            VALUES ('{CompanyName}', \"{WebSite}\", \"{CompanyDescription}\", \"{DefaultAddress}\", '{Interests}', '{Products}', '{Projects}')"
        try:
            self.cursor.execute(sql)
            companyId=self.conn.insert_id()
            self.conn.commit()
            return companyId
        except Exception as e:
            self.conn.rollback()
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            raise e

    def insert_capabilities_am(self, data):
        self.test_connection()
        sql = "insert into capability_am(CompanyID,CapCode) values (%s,%s);"
        try:
            self.cursor.executemany(sql, data)
            self.conn.commit()
            LOGGER.debug(
                f"MYSQL loads data to capability_am table successfully")
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")

    def delete_data_by_id(self, table, column, ids):
        self.test_connection()
        sql = f"DELETE FROM {table} WHERE {column}=%s"
        try:
            self.cursor.executemany(sql, ids)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")

    def search_am_by_mids(self, mids):
        self.test_connection()
        str_ids = str(mids).replace('[', '').replace(']', '')
        sql = "select * from am where mid in (" + str_ids + \
            ") order by field (mid, " + str_ids + ");"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            LOGGER.debug("MYSQL search by milvus id.")
            return results
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")

    def get_am_by_company_name(self, company_name):
        # get all the info of designated table
        self.test_connection()
        sql = f"SELECT * FROM `am` WHERE CompanyName LIKE '%{company_name}%'"
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            raise e

    def get_mid_by_company_id(self, company_id):
        self.test_connection()
        sql = f"SELECT mid FROM `am` WHERE CompanyID={company_id}"
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            raise e

    def get_cap_code_by_company_id(self, company_id):
        self.test_connection()
        sql = f"SELECT capability_am.CapCode FROM capability_am WHERE CompanyID = {company_id}"
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            raise e

    def get_am_by_mid_and_cap_code(self, mids, sql_like_addition):
        self.test_connection()
        str_ids = str(mids).replace('[', '').replace(']', '')
        sql = f"SELECT DISTINCT am.* FROM am JOIN capability_am \
            ON am.CompanyID = capability_am.CompanyID \
            WHERE am.mid IN ({str_ids}) AND ({sql_like_addition}) ORDER BY FIELD(mid,{str_ids})"
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            raise e

    def get_all_capability(self):
        self.test_connection()
        sql = "SELECT * FROM `capability`"
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            raise e

    def get_all_data(self, table):
        self.test_connection()
        sql = f"SELECT * FROM {table}"
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def get_all_data_from_am(self):
        return self.get_all_data('am')

    def get_newest_10(self, table, order_col):
        self.test_connection()
        sql = f"SELECT * FROM {table} ORDER BY {order_col} DESC LIMIT 10 "
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def get_newest_10_from_am(self):
        return self.get_newest_10('am', 'CompanyID')

    def search_by_column(self, table, column, values_str):
        # according to the designated field, search designated table
        self.test_connection()
        sql = f"SELECT * FROM {table} WHERE {column} in {values_str}"
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def load_data_to_mysql(self, table_name, data):
        self.test_connection()
        sql = "insert into " + table_name + \
            " (milvus_id,title,text) values (%s,%s,%s);"
        try:
            self.cursor.executemany(sql, data)
            self.conn.commit()
            LOGGER.debug(
                f"MYSQL loads data to table: { table_name} successfully")
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def delete_table(self, table_name):
        # Delete mysql table if exists
        self.test_connection()
        sql = "drop table if exists " + table_name + ";"
        try:
            self.cursor.execute(sql)
            LOGGER.debug(f"MYSQL delete table:{table_name}")
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def delete_all_data(self, table_name):
        # Delete all the data in mysql table
        self.test_connection()
        sql = 'delete from ' + table_name + ';'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            LOGGER.debug(f"MYSQL delete all data in table:{table_name}")
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def count_table(self, table_name):
        # Get the number of mysql table
        self.test_connection()
        sql = "select count(milvus_id) from " + table_name + ";"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            LOGGER.debug(f"MYSQL count table:{table_name}")
            return results[0][0]
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)
