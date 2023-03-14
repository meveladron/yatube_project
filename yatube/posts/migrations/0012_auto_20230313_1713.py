# Generated by Django 2.2.16 on 2023-03-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20230310_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default=1, help_text='Введите название публикации', max_length=200, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(help_text='Введите название группы', max_length=200, verbose_name='Название'),
        ),
    ]
