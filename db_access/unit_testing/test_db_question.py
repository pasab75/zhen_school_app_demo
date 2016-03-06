from db_access.db_question import database_access
import business_objects.question as question_obj_generator


db = database_access()
db_record_to_be_saved = question_obj_generator.question(None,"Is zhen a nice guy",
                                    "No",
                                    "Maybe",
                                    "Yes",
                                    "Why are you asking me this",
                                    "DERPDERP",
                                    5)
db_success = db.save_new_question(db_record_to_be_saved)
print(db_success)
assert db_success is True
db.close_connection()

#TODO Add a unit test for deleting a record, updating a record, and pulling a record by id and other fields