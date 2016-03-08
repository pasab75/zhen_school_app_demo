from db_access.db_question import database_access
import business_objects.question as question_obj_generator

#test to see we can make a new record
db = database_access()

original_question = question_obj_generator.question(None, "Is zhen a nice guy",
                                    "No",
                                    "Maybe",
                                    "Yes",
                                    "Why are you asking me this",
                                    "DERPDERP",
                                    "Herp",
                                    "Chapter 1",
                                    "Zhen Trivia",
                                    5)

db_success = db.save_new_question(original_question)
print(db_success)
assert db_success is True

#test to make sure we can query by message text

new_question_obj = db.get_by_question_text(original_question.get_question_text())

assert original_question.get_question_text() == new_question_obj.get_question_text()

#test to make sure we can query by question id
id = new_question_obj.get_question_id()
new_question_obj.set_question_text("Is zhen a douche?")
db.update_question(new_question_obj)
test_query_obj = db.get_by_id(id)
assert test_query_obj.get_question_id() == new_question_obj.get_question_id()

#now delete the record
db.delete_question(id)
db.close_connection()

#TODO Add a unit test for deleting a record, updating a record, and pulling a record by id and other fields