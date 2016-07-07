from flask import jsonify
import db_access.db_words as db_wordzors


class Word:
    _word_index = None
    _word = None
    _chapter_index = None
    _instructor_difficulty = False
    _calculated_difficulty = None
    _avg_answer_time = None

    def __init__(self,
                 index=None,
                 word=None,
                 chapter_index=None,
                 instructor_difficulty=None,
                 calculate_difficulty=None,
                 avg_answer_time=None):

        self._word_index = index
        self._word = word
        self._chapter_index = chapter_index
        self._instructor_difficulty = instructor_difficulty
        self._calculated_difficulty = calculate_difficulty
        self._avg_answer_time = avg_answer_time

    def get_jsonified(self):
        return jsonify(
            word_index = self._word_index,
            word = self._word,
            chapter_index = self._chapter_index,
            instructor_difficulty = self._instructor_difficulty,
            calculated_difficulty = self._calculated_difficulty,
            avg_answer_time = self._avg_answer_time
            )

    def get_database_format(self):
        return {
            'word_index': self._word_index,
            'word': self._word,
            'chapter_index': self._chapter_index,
            'instructor_difficulty': self._instructor_difficulty,
            'calculated_difficulty': self._calculated_difficulty,
            'avg_answer_time': self._avg_answer_time
        }


    def set_from_database(self, word):
        self._word_index = word['word_index']
        self._word = word['word']
        self._chapter_index = word['chapter_index']
        self._instructor_difficulty = word['instructor_difficulty']
        self._calculated_difficulty = word['calculated_difficulty']
        self._avg_answer_time = word['avg_answer_time']

    def generate_word_randomly(self, chapter=None):
        db_word = db_wordzors.WordTableAccess()
        if chapter:
            self.set_from_database(db_word.get_word_random_by_chapter(chapter))
        else:
            self.set_from_database(db_word.get_word_random())
        db_word.close_connection()

    def generate_word_randomly_chapter_index(self, index):
        db_word = db_wordzors.WordTableAccess()
        self.set_from_database(db_word.get_word_random_by_chapter_index(index))
        db_word.close_connection()

    def get_word(self):
        return self._word

    def get_index(self):
        return self._word_index

    def set_index(self, index):
        self._word_index = index

    def get_chapter_index(self):
        return self._chapter_index

    def set_chapter_index(self, index):
        self._chapter_index = index

    # only call this if you're sure this doesn't exist in the db already
    def save_new(self):
        try:
            db_word = db_wordzors.WordTableAccess()
            db_word.save_new_word_from_object(self.get_database_format())
            db_word.close_connection()
            return True
        except Exception as e:
            print("Could not delete question: " + str(e))
            return False
