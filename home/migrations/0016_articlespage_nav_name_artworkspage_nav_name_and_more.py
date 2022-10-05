# Generated by Django 4.0.6 on 2022-10-05 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_article_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlespage',
            name='nav_name',
            field=models.CharField(default='Accueil', help_text="Ce nom d'affichera dans la barre de navigation", max_length=36, verbose_name='Nom dans le menu'),
        ),
        migrations.AddField(
            model_name='artworkspage',
            name='nav_name',
            field=models.CharField(default='Accueil', help_text="Ce nom d'affichera dans la barre de navigation", max_length=36, verbose_name='Nom dans le menu'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='nav_name',
            field=models.CharField(default='Accueil', help_text="Ce nom d'affichera dans la barre de navigation", max_length=36, verbose_name='Nom dans le menu'),
        ),
        migrations.AddField(
            model_name='presentationpage',
            name='nav_name',
            field=models.CharField(default='Accueil', help_text="Ce nom d'affichera dans la barre de navigation", max_length=36, verbose_name='Nom dans le menu'),
        ),
        migrations.AddField(
            model_name='workexperiencepage',
            name='nav_name',
            field=models.CharField(default='Accueil', help_text="Ce nom d'affichera dans la barre de navigation", max_length=36, verbose_name='Nom dans le menu'),
        ),
    ]
