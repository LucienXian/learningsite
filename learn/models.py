from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
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

class LearningPlan(models.Model):
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    wordbook = models.ForeignKey(WordBook, verbose_name=u"单词本", on_delete=models.CASCADE)

    class Meta:
        verbose_name = u"学习计划"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"{0} - {1}".format(self.user.username, self.wordbook)

class LearningRecord(models.Model):
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    wordbook = models.ForeignKey(WordBook, verbose_name=u"单词本", on_delete=models.CASCADE)    
    islearning = models.IntegerField(default=0, verbose_name=u"正在学习")
    learn_time = models.DateTimeField(default=datetime.now,
                                      verbose_name=u"学习时间")
    duration = models.IntegerField(default=0, verbose_name=u"学习时长")
    correct_rate = models.IntegerField(default=100, verbose_name=u"正确率")
    haslearned = models.IntegerField(default=0, verbose_name=u"已经学习")

    class Meta:
        verbose_name = u"学习记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"{0} - isornotlearning{1}".format(self.user.username, self.islearning)

class UserSetting(models.Model):
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    dailyword = models.IntegerField(default=50, verbose_name=u"每日学习量")
    showmeaning = models.IntegerField(default=1, verbose_name=u"英文解释")
    learntype = models.IntegerField(default=1, verbose_name=u"单词的目标掌握程度")

    class Meta:
        verbose_name = u"用户设置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"{0} - {1}".format(self.user.username, self.dailyword)

class UserDefWords(models.Model):
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    word = models.ForeignKey(Word, verbose_name = u"单词", on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name = u"用户自定义单词"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"{0} - {1}".format(self.user.username, self.word.spelling)