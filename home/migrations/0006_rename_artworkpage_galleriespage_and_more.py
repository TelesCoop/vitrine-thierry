# Generated by Django 4.0.6 on 2022-07-09 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0069_log_entry_jsonfield'),
        ('home', '0005_gallery_color'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ArtworkPage',
            new_name='ArtworksPage',
        ),
        migrations.AlterModelOptions(
            name='artworkspage',
            options={'verbose_name': 'Page des galleries', 'verbose_name_plural': 'Pages des galleries'},
        ),
    ]