# Generated by Django 4.1.7 on 2023-03-15 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='preview',
            field=models.ImageField(null=True, upload_to='media/images/'),
        ),
    ]