# Generated by Django 2.0.7 on 2018-07-17 09:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20180717_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='attempt_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='option',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('image', 'Image')], max_length=50),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('multiple-choice', 'Multiple Choice'), ('fill-in-the-blanks', 'Fill In The Blanks')], max_length=50),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='marks_secured',
            field=models.IntegerField(default=0),
        ),
    ]
