# Generated by Django 4.0.3 on 2022-05-11 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_traindetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='traindetail',
            name='availableOn',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
    ]
