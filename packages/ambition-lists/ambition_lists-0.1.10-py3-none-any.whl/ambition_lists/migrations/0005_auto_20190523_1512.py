# Generated by Django 2.2 on 2019-05-23 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ambition_lists', '0004_arvregimens'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='arvregimens',
            options={'ordering': ['display_index', 'name']},
        ),
        migrations.AlterModelOptions(
            name='infiltratelocation',
            options={'ordering': ['display_index', 'name']},
        ),
        migrations.AlterModelOptions(
            name='misseddoses',
            options={'ordering': ['display_index', 'name']},
        ),
    ]
