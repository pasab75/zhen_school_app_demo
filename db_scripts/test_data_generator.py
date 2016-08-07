from random import randint

import business_objects.Chapter as Chapter
import business_objects.Definition as Definition
import business_objects.Reward as Reward
import business_objects.deprecated.Classroom as Classroom

import deprecated_files.business_objects.Word as Word

# choose random entries or looped entries
random = False

# loads random numbers of chapters/words/definitions
if random:
    num_chapters = randint(10, 40)
    num_words = randint(10, 200)*num_chapters
    num_definitions_per_word = randint(2, 10)

    for i in range(1, num_chapters+1):
        chapter_name = "This is Chapter " + i
        new_chapter = Chapter.Chapter(index=i, chapter_name=chapter_name)

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
    word_index = 0
    for i in range(1, num_chapters+1):
        chapter_name = "This is Chapter " + str(i)
        new_chapter = Chapter.Chapter(chapter_index=i, chapter_name=chapter_name)
        result = new_chapter.save_new()
        if not result:
            raise Exception("Hey this didn't work, nothing else will work either")
        for j in range(1, num_words_per_chapter+1):
            word_index += 1
            word_string = "word " + str(word_index) + " chapter " + str(i)
            new_word = Word.Word(index=word_index, word=word_string, chapter_index=i)
            new_word.save_new()

            for k in range(1, num_definitions_per_word+1):
                k = str(k)
                definition_string = "I am definition number "\
                                    + str(k) + \
                                    " for word number " + str(word_index) + \
                                    " in chapter number " + str(i) + "."
                new_definition = Definition.Definition(word_index=word_index,
                                                       definition=definition_string,
                                                       chapter_index=i)
                new_definition.save_new()

class_code = 'A1B2C3D4E5'

new_classroom = Classroom.Classroom(class_code, 4, 3)
new_classroom.save_new()

for i in range(10):
    index = i+1
    reward_name = "Reward " + str(index)
    reward_description = "This is reward number " + str(index) + ", I'm sure it does something good."
    required_points = index*1000
    new_reward = Reward.Reward(
        class_code=class_code,
        reward_name=reward_name,
        reward_description=reward_description,
        required_points=required_points
    )
    new_reward.save_new()
