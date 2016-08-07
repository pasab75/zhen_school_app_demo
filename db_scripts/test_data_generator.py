from random import randint

from business_objects.Models import *


class_code = 'A1B2C3D4E5'
# choose random entries or looped entries
random = False

# loads random numbers of chapters/words/definitions
if random:
    num_chapters = randint(5, 20)
    num_words = randint(10, 100)*num_chapters
    num_definitions_per_word = randint(2, 10)

    for i in range(1, num_chapters+1):
        chapter_name = "This is Chapter " + i
        new_chapter = Chapter(index=i, chapter_name=chapter_name)
        new_chapter.save()

    for i in range(1, num_words+1):
        chapter_index = randint(1, num_chapters+1)
        word_string = "word " + i
        word_index = i+1
        new_word = Word(word_index=word_index, word=word_string, chapter_index=chapter_index)
        new_word.save()
        for k in range(1, num_definitions_per_word+1):
            definition_string = "I am definition number " \
                                + k + \
                                " for word number " + i + "."
            new_definition = Definition(
                word_index=word_index,
                chapter_index=chapter_index,
                definition=definition_string
            )
            new_definition.save()

# loads set numbers of chapters/words/definitions
else:
    num_chapters = 10
    num_words_per_chapter = 50
    num_definitions_per_word = 5
    word_index = 0
    for i in range(1, num_chapters+1):
        chapter_name = "This is Chapter " + str(i)
        new_chapter = Chapter(chapter_index=i, chapter_name=chapter_name)
        result = new_chapter.save()
        if not result:
            raise Exception("Hey this didn't work, nothing else will work either")
        for j in range(1, num_words_per_chapter+1):
            word_index += 1
            word_string = "word " + str(word_index) + " chapter " + str(i)
            new_word = Word(index=word_index, word=word_string, chapter_index=i)
            new_word.save()

            for k in range(1, num_definitions_per_word+1):
                k = str(k)
                definition_string = "I am definition number "\
                                    + str(k) + \
                                    " for word number " + str(word_index) + \
                                    " in chapter number " + str(i) + "."
                new_definition = Definition(
                    word_index=word_index,
                    definition=definition_string,
                    chapter_index=i
                )
                new_definition.save()

new_classroom = Classroom(
    class_code=class_code,
    current_chapter=4,
    number_dailies_allowed=3,
    max_multiplier=5,
    daily_exp_base=30
)
new_classroom.save()

for i in range(10):
    index = i+1
    reward_name = "Reward " + str(index)
    reward_description = "This is reward number " + str(index) + ", I'm sure it does something good."
    required_points = index*1000
    new_reward = Reward(
        class_code=class_code,
        reward_name=reward_name,
        reward_description=reward_description,
        required_points=required_points
    )
    new_reward.save()
