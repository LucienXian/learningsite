from django.db import models
from account.models import User
# Create your models here.
class Word(models.Model):
    spelling = models.CharField(blank=False, max_length=100, verbose_name = u"拼写")
    meaning = models.CharField(blank=False, max_length=300, verbose_name=u"解释")
    mp3_url = models.URLField(blank=True, verbose_name="mp3")

    class Meta:
        verbose_name = u"单词"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.spelling


class WordBook(models.Model):
    title = models.CharField(blank=True, max_length=50,
                                   verbose_name=u"书名")
    description = models.CharField(blank=True, max_length=200,
                                   verbose_name=u"描述")
    uploaded_user = models.ForeignKey(User, verbose_name=u"上传人", on_delete=models.CASCADE)
    word_num = models.IntegerField(default=1000, verbose_name=u"单词数")

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = u"单词本"
        verbose_name_plural = verbose_name

class WordUnit(models.Model):
    book = models.ForeignKey(WordBook, verbose_name = u"单词本", on_delete=models.CASCADE)
    unit_order = models.IntegerField(default=1, verbose_name=u"顺序")
    word_num = models.IntegerField(default=2000, verbose_name=u"单词数")

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"{0} - unit {1}".format(self.book.title, self.unit_order)

    class Meta:
        verbose_name = u"单元"
        verbose_name_plural = verbose_name

class WordInUnit(models.Model):
    word = models.ForeignKey(Word, verbose_name = u"单词", on_delete=models.DO_NOTHING)
    wordunit = models.ForeignKey(WordUnit, verbose_name=u"单元", on_delete=models.CASCADE)
    word_order = models.IntegerField(default=1, verbose_name=u"顺序")

    class Meta:
        verbose_name = u"单元单词"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"{0} - unit {1}".format(self.word, self.wordunit)
