# Generated by Django 2.0.3 on 2018-06-28 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0007_remove_learningplan_haslearned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='learntype',
            field=models.IntegerField(default=1, verbose_name='单词的目标掌握程度'),
        ),
    ]