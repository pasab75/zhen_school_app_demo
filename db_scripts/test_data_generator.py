import business_objects.Word as Word
import business_objects.Definition as Definition
import business_objects.Chapter as Chapter
from random import randint

# choose random entries or looped entries
random = False

# loads random numbers of chapters/words/definitions
if random:
    num_chapters = randint(10, 40)
    num_words = randint(10, 200)*num_chapters
    num_definitions_per_word = randint(2, 10)

    for i in range(1, num_chapters+1):
        chapter_name = "This is Chapter " + i
        new_chapter = Chapter.Chapter(index=i,chapter_name=chapter_name)

    for i in range(1, num_words+1):
        chapter_index = randint(1, num_chapters+1)
        word_string = "word " + i
        new_word = Word.Word(word=word_string, chapter_index=chapter_index)
        new_word.save_new()
        for k in range(1, num_definitions_per_word+1):
            definition_string = "I am definition number " \
                                + k + \
                                " for word number " + i + "."
            new_definition = Definition.Definition(definition=definition_string)
            new_definition.save_new()

# loads set numbers of chapters/words/definitions
else:
    num_chapters = 25
    num_words_per_chapter = 100
    num_definitions_per_word = 5

    for i in range(1,num_chapters+1):
        chapter_name = "This is Chapter " + str(i)
        new_chapter = Chapter.Chapter(chapter_index=i,chapter_name=chapter_name)
        result = new_chapter.save_new()
        if not result:
            raise Exception("Hey this didn't work, nothing else will work either")
        for j in range(1, num_words_per_chapter+1):
            word_string = "word " + str(j) + " chapter " + str(i)
            new_word = Word.Word(word=word_string,chapter_index=i)
            new_word.save_new()

            for k in range(1, num_definitions_per_word+1):
                k = str(k)
                definition_string = "I am definition number "\
                                    + str(k) + \
                                    " for word number " + str(j) + \
                                    " in chapter number " + str(i) + "."
                new_definition = Definition.Definition(word_index=j, definition=definition_string, chapter_index=i)
                new_definition.save_new()
