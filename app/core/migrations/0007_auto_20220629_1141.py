# Generated by Django 3.2.13 on 2022-06-29 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_recipe_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['-name'], 'verbose_name': 'Ingredient', 'verbose_name_plural': 'Ingredients'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-id'], 'verbose_name': 'Recipe', 'verbose_name_plural': 'Recipes'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-name'], 'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
    ]
