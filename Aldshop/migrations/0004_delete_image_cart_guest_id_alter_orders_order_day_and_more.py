# Generated by Django 4.1.2 on 2022-11-21 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aldshop', '0003_image_alter_orders_order_day_alter_users_signup_day'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='cart',
            name='guest_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='Order_day',
            field=models.CharField(default=21, max_length=100),
        ),
        migrations.AlterField(
            model_name='users',
            name='signup_day',
            field=models.CharField(default=21, max_length=50),
        ),
    ]