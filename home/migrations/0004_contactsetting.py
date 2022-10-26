# Generated by Django 4.0.6 on 2022-10-26 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0077_alter_revision_user'),
        ('home', '0003_alter_workexperiencepage_parcours_block_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(default='thierry.baudry.glass@wanadoo.fr', max_length=128, verbose_name='Email de contact')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': 'Contact',
            },
        ),
    ]