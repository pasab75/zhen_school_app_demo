import business_objects.Word as Word
import business_objects.Definition as Definition
import business_objects.Chapter as Chapter
from random import randint

# choose random entries or looped entries
random = False

if random:

    num_chapters = randint(10, 40)
    num_words = randint(10, 200)*num_chapters
    num_definitions_per_word = randint(2, 10)

    for i in range(1, num_chapters+1):
        chapter_name = "This is Chapter " + i
        new_chapter = Chapter.Chapter(index=i,chapter_name=chapter_name)

    for i in range(1, num_words+1):
        chapter_index = randint(1,num_chapters+1)
        word_string = "word " + i
        new_word = Word.Word(word=word_string, chapter_index=chapter_index)
        new_word.save_new()
        for k in range(1, num_definitions_per_word+1):
            definition_string = "I am definition number " \
                                + k + \
                                " for word number " + j + \
                                " in chapter number " + i + "."
            new_definition = Definition.Definition(definition=definition_string)
            new_definition.save_new()

else:
    # load chapter_database
    for i in range(1,26):
        chapter_name = "This is Chapter " + i
        new_chapter = Chapter.Chapter(index=i,chapter_name=chapter_name)

        for j in range(1,101):
            word_string = "word " + j + " chapter " + i
            new_word = Word.Word(word=word_string,chapter_index=i)
            new_word.save_new()

            for k in range(1,5):
                definition_string = "I am definition number "\
                                    + k + \
                                    " for word number " + j + \
                                    " in chapter number " + i +"."
                new_definition = Definition.Definition(definition=definition_string)
                new_definition.save_new()
