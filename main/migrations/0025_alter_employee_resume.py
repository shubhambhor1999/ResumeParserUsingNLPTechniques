# Generated by Django 3.2.3 on 2021-05-16 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_employee_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='resume',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]