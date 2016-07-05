from flask import jsonify
import db_access.db_topic_chapter as database


class TopicChapter:
    _chapter = None
    _chapter_name = None
    _topic_name = None
    _topic_index = None

    def __init__(self,
                 chapter=None,
                 chapter_name=None,
                 topic_name=None,
                 topic_index=None
                 ):

        self._chapter = chapter
        self._chapter_name = chapter_name
        self._topic_index = topic_index
        self._topic_name = topic_name

    def get_jsonified(self):
        return jsonify(
            chapter = self._chapter,
            chapter_name = self._chapter_name,
            topic_index = self._topic_index,
            topic_name = self._topic_name
            )

    def get_database_format(self):
        return {
            'chapter': self._chapter,
            'chapter_name': self._chapter_name,
            'topic_index': self._topic_index,
            'topic_name': self._topic_name
        }