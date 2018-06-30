import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learningsite.settings")

import django
django.setup()

import csv

def main():
    from learn.models import Word, WordBook, WordUnit, WordInUnit
    with open('crawler_words/kaoyan.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        WordunitList = []
        order = 0
        unit_order = 1
        get_book = WordBook.objects.get(title='test3')
        unit = WordUnit.objects.create(book=get_book, unit_order=unit_order)

        for row in spamreader:
            order += 1
            if order > 200:
                unit.word_num = order-1
                order = 1
                unit_order += 1
                unit = WordUnit.objects.create(book=get_book, unit_order=unit_order)
            word = Word.objects.create(spelling=row[0], meaning=row[1])
            wordofunit = WordInUnit(word=word, wordunit=unit, word_order=unit_order)
            print(row[0], row[1])
            # word = word(spelling=row[0], meaning=row[1])
            WordunitList.append(wordofunit)
        unit.word_num = order
        WordInUnit.objects.bulk_create(WordunitList)
 
if __name__ == "__main__":
    main()
    print('Done!')