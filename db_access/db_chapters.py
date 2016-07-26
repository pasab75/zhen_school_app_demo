from db_access.db_general import GeneralDatabaseConnection

table_name = "chapters"


class ChapterTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        GeneralDatabaseConnection.__init__(self)

    # -------------------------------------------------------------
    # GET methods
    # -------------------------------------------------------------

    def get_chapter_by_index(self, index):
        try:
            try:
                db_obj = self.get_row_by_key_value(table_name, "chapter_index", index)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_chapter_random(self):
        try:
            try:
                db_obj = self.get_row_random(table_name)

                return db_obj
            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_chapter_random_with_limits(self, lower, upper):
        try:
            try:
                db_obj = self.get_row_random_with_limits(table_name, "index", lower, upper)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_chapters_total(self):
        try:
            try:
                db_obj = self.get_numrows(table_name)
                return db_obj['COUNT(*)']
            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    def update_chapter_by_index(self, chapter, index):
        try:
            self.update_row_in_table(chapter.get_database_format, table_name, index)
        except Exception as e:
            print("Could not update chapter" + str(e))
            return False

    # deletes a chapter from the database using its index
    def delete_chapter_by_index(self, index):
        try:
            self.delete_row_in_table_with_attribute(table_name, 'index', index)
        except Exception as e:
            print("Could not delete chapter: " + str(e))

    def save_new_chapter_from_object(self, chapter):
        try:
            self.save_new_row_in_table(chapter, table_name)

        except Exception as e:
            print("Could not save question: " + str(e))
            return False