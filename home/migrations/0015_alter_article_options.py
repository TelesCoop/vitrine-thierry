# Generated by Django 4.0.6 on 2022-10-05 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_articlespage_alter_article_pdf'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-created'], 'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
    ]
