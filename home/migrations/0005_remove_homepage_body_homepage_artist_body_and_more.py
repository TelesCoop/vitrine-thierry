# Generated by Django 4.0.6 on 2022-07-28 16:02

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('home', '0004_alter_workexperiencepage_parcours_block_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='body',
        ),
        migrations.AddField(
            model_name='homepage',
            name='artist_body',
            field=wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='artist_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='artist_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='workexperiencepage',
            name='parcours_block_data',
            field=wagtail.fields.StreamField([('chapters', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre')), ('steps', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('date', wagtail.blocks.CharBlock(label='Date', required=False)), ('richtext', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], label='Description'))], label='Les différentes étapes de ton parcours', label_format='{date}'), label='Etapes'))], label='Parties de ton parcours', label_format='{title}'))], blank=True, use_json_field=None, verbose_name='Parcours'),
        ),
    ]