# Generated by Django 3.0.7 on 2020-12-07 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200706_1027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogger',
            options={'ordering': ['-nickname'], 'permissions': [('is_blogger', 'is Blogger')]},
        ),
    ]
