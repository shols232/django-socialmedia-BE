# Generated by Django 3.1.2 on 2020-11-28 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_comment_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='replies',
            field=models.ManyToManyField(to='posts.Reply'),
        ),
    ]