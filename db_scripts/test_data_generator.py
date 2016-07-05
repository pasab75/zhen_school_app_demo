import business_objects.Word as Word
import business_objects.Definition as Definition
from random import randint

#load chapter_index database
for i in range(25):
    i = 10

#load word database
for i in range(1000):
    topic_index = randint(0, 500)
    word_string = "word number " + i
    new_word = Word.Word(word=word_string, topic_index=topic_index)
    new_word.save_new()


#load definitions database
for i in range(1000):
    for j in range(5):
        definition_string = "I am definition number " + j + " for word number " + i + "."
        new_definition = Definition.Definition(definition=definition_string)
        new_definition.save_new()