# Generated by Django 3.2.6 on 2021-09-07 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global_app', '0002_auto_20210907_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='A1',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='A2',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='B1',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='B2',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='C1',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='C2',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='D',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='main',
            field=models.FileField(upload_to=''),
        ),
    ]
