from db_access.db_general import GeneralDatabaseConnection

table_name = "classrooms"


class ClassroomTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        GeneralDatabaseConnection.__init__(self)

    # -------------------------------------------------------------
    # fetch db_obj methods
    # -------------------------------------------------------------

    def get_classroom_by_class_code(self, class_code):
        try:
            try:
                db_obj = self.get_row_by_key_value(table_name, "class_code", class_code)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    # -------------------------------------------------------------
    # Write Methods
    # -------------------------------------------------------------

    def save_new_classroom_from_object(self, classroom):
        try:
            self.save_new_row_in_table(classroom.get_database_format(), table_name)

        except Exception as e:
            print("Could not save classroom: " + str(e))
            return False

    def update_classroom_by_index(self, classroom, class_code):
        try:
            self.update_row_in_table(classroom.get_database_format(), table_name, class_code)
        except Exception as e:
            print("Could not update classroom" + str(e))
            return False

    # deletes a chapter from the database using its index
    def delete_classroom_by_index(self, class_code):
        try:
            self.delete_row_in_table_with_attribute(table_name, 'class_code', class_code)
        except Exception as e:
            print("Could not delete classroom: " + str(e))