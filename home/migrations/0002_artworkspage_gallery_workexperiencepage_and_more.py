# Generated by Django 4.0.6 on 2022-07-27 07:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import wagtail.blocks
import wagtail.contrib.routable_page.models
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('wagtailcore', '0069_log_entry_jsonfield'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtworksPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'Page des galeries',
                'verbose_name_plural': 'Pages des galeries',
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('color', models.CharField(choices=[('gallery-blue', 'Bleue'), ('gallery-purpule', 'Violet'), ('gallery-orange', 'Orange'), ('gallery-cyan', 'Cyan'), ('gallery-green', 'Vert'), ('gallery-yellow', 'Jaune'), ('gallery-red', 'Rouge')], default='gallery-blue', help_text='Choisir la couleur de la galerie', max_length=32)),
            ],
            options={
                'verbose_name': 'Galerie',
            },
        ),
        migrations.CreateModel(
            name='WorkExperiencePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Introduction de la page parcours')),
                ('parcours_block_data', wagtail.fields.StreamField([('chapters', wagtail.blocks.StructBlock([('subtitle', wagtail.blocks.CharBlock(label='Sous titre')), ('steps', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('date', wagtail.blocks.CharBlock(blank=True, label='Date', null=True)), ('richtext', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], label='Description'))], label='Les différentes étapes de ton parcours', label_format='{date}')))], label='Parties de ton parcours', label_format='{subtitle}'))], blank=True, use_json_field=None, verbose_name='Membres du Comité - contenu')),
            ],
            options={
                'verbose_name': 'Page de presentation',
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.AlterModelOptions(
            name='homepage',
            options={'verbose_name': "Page d'Accueil"},
        ),
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.RichTextField(blank=True, null=True, verbose_name="Contenu de la page d'accueil"),
        ),
        migrations.CreateModel(
            name='PresentationPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Contenu de la page de présentation')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Page de presentation',
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='BannerSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navbar_banner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Image')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': 'Banière-image',
            },
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title', label='Titre')), ('richtext', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], label='Paragraphe')), ('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('pdf', wagtail.documents.blocks.DocumentChooserBlock(label='PDF'))], blank=True, help_text='Corps de la page', use_json_field=None, verbose_name='Contenu')),
                ('name', models.CharField(max_length=100, verbose_name="Nom de l'oeuvre")),
                ('slug', models.SlugField(blank=True, default='', max_length=100, unique=True, verbose_name='Slug (URL de la ressource)')),
                ('short_description', models.CharField(max_length=256, verbose_name='Description courte')),
                ('galleries', models.ManyToManyField(blank=True, related_name='artworks', to='home.gallery', verbose_name='Galeries')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Image principale')),
            ],
            options={
                'verbose_name': 'Oeuvre',
                'verbose_name_plural': 'Oeuvres',
                'ordering': ['-created'],
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]