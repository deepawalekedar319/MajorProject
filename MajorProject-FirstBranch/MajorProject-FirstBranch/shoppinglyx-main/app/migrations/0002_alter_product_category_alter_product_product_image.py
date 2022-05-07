# Generated by Django 4.0.3 on 2022-04-19 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('M', 'Mobile'), ('L', 'Laptop'), ('TW', 'Top Wear'), ('BW', 'Bottom Wear'), ('EL', 'Electronics'), ('GE', 'Gym'), ('HA', 'House Appliances'), ('MS', 'Medical Store'), ('RM', 'Raw Materials'), ('JL', 'Jewellery'), ('TS', 'Toys')], max_length=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to='producting'),
        ),
    ]
