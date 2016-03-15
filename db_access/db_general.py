import pymysql.cursors


class GeneralDatabaseConnection:

    # -------------------------------------------------------------
    # class variables
    # -------------------------------------------------------------

    db_connection = None

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        print("connected")
        self.db_connection = pymysql.connect(host='localhost',
                                            user='appuser',
                                            password='carhorsebatterysuccess',
                                            db='testdb',
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor,
                                            autocommit=True
                                            )

    # As a rule of thumb, all values that can be thought of as text input from the API should never
    # be concatenated into a SQL query directly. Instead, they should be passed as arguments to the execution
    # method. I've rewritten most, if not all, methods to reflect this

    # -------------------------------------------------------------
    # general methods
    # -------------------------------------------------------------

    # -------------------------------------------------------------
    # READ methods
    # -------------------------------------------------------------

    def get_row_by_key_value(self, table, key, value):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT FROM {} WHERE '{}' = {}".format(table, key, '%s')
                    cursor.execute(sql, value)

                    return cursor.fetchone()

            except Exception as ex:
                print("error adding row to table :" + str(ex))
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def get_rows_by_key_value(self, table, key, value):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT FROM {} WHERE '{}' = {}".format(table, key, '%s')
                    cursor.execute(sql, value)

                    return cursor.fetchall()

            except Exception as ex:
                print("error adding row to table :" + str(ex))
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    # this method adds a dictionary of key-value pairs to the database
    # the valuelist is an ordered list of values that correspond to the field names
    # table is the name of the table that you are putting the row in
    def save_new_row_in_table(self, dictionary_to_add, table):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    placeholders = ', '.join(['%s'] * len(dictionary_to_add))
                    columns = ", ".join(dictionary_to_add.keys())
                    sql = "INSERT INTO {} ( {} ) VALUES ( {} )".format(table, columns, placeholders)

                    cursor.execute(sql, list(dictionary_to_add.values()))

                    return True

            except Exception as ex:
                print("error adding row to table :" + str(ex))
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    # this method updates an existing row with key-value pairs given by the dictionary
    # table is the name of the table that you are searching in
    # primary should be an index of the primary key that you are search with
    # THE PRIMARY KEY WILL NOT BE UPDATED
    def update_row_in_table(self, dictionary_to_add, table, primary):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    # removes the primary search key and value
                    searchvalue = dictionary_to_add[primary]
                    del dictionary_to_add[primary]

                    keystring = '={}, '.join(dictionary_to_add.keys()) + '={}'

                    sql = "UPDATE {} SET {} WHERE '{}'=%s" .format(table, keystring, primary, searchvalue)

                    # executes the sql code with list of values to update as a parameter
                    cursor.execute(sql, dictionary_to_add.values())

                    return True
            except Exception as e:
                print("Error updating row: "+str(e))
                return False
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def delete_row_in_table_with_attribute(self, table, field, value):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "DELETE FROM %s WHERE %s = %s"
                    args = (table, field, value)
                    cursor.execute(sql, args)

                    return True
            except Exception as e:
                print("Error fetching results: "+str(e))
                return False
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def close_connection(self):
        self.db_connection.close()

    # -------------------------------------------------------------
    # debug methods
    # -------------------------------------------------------------

    # empties all rows from the questions table
    # currently the front end requests that the questions table gets emptied every time and is replaced by new
    # randomly generated questions
    def empty_table(self, table):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "DELETE FROM %s" % table
                    cursor.execute(sql)

            except Exception as e:
                print("Error emptying table "+str(e))
        except Exception as e:
            print("Error while connecting "+str(e))

    # returns the number of rows in any table
    def get_numrows(self, table):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    question = None
                    sql = "SELECT COUNT(*) FROM %s"
                    cursor.execute(sql, table)
                    request = cursor.fetchone()
                    print(request)

            except Exception as e:
                print("Error counting rows "+str(e))
        except Exception as e:
            print("Error while connecting "+str(e))
