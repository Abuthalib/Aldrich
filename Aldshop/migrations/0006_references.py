# Generated by Django 4.1.2 on 2022-11-23 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aldshop', '0005_alter_orders_order_day_alter_users_signup_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='References',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('refered_user_id', models.CharField(max_length=100)),
            ],
        ),
    ]