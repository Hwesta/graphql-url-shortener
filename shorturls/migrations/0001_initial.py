# Generated by Django 2.2.2 on 2019-06-19 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URLMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.CharField(help_text='URL to redirect to (max 2000 characters)', max_length=2000)),
                ('short_url', models.CharField(help_text='Short URL string', max_length=20, unique=True)),
            ],
        ),
    ]
