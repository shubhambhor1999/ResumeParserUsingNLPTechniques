# Generated by Django 3.0.7 on 2020-06-26 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200626_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='job_title',
        ),
        migrations.AddField(
            model_name='employee',
            name='job_title',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.CharField(max_length=300),
        ),
    ]