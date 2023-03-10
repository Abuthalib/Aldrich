# Generated by Django 4.1.2 on 2022-12-02 04:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Aldshop', '0007_alter_orders_order_day_alter_orders_order_month_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.CharField(default='amal', max_length=100)),
                ('discount_percentage', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('coupon_code', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='products',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='users',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='products',
            name='manufacturing_date',
            field=models.CharField(default=datetime.date(2022, 12, 2), max_length=100),
        ),
        migrations.AddField(
            model_name='users',
            name='wallet_balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orders',
            name='Order_day',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='orders',
            name='Order_month',
            field=models.IntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='orders',
            name='Order_year',
            field=models.IntegerField(default=2022),
        ),
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='products',
            name='image_1',
            field=models.ImageField(upload_to='image_1_of_products/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image_2',
            field=models.ImageField(upload_to='image_2_of_products/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image_3',
            field=models.ImageField(upload_to='image_3_of_products/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image_4',
            field=models.ImageField(upload_to='image_4_of_products/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='products',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='products',
            name='total_sold',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='users',
            name='signup_day',
            field=models.CharField(default=2, max_length=50),
        ),
        migrations.CreateModel(
            name='Wallet_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=1, max_length=100)),
                ('reason', models.CharField(max_length=500)),
                ('Debit_Credit', models.CharField(default='credited', max_length=500)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aldshop.orders')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aldshop.category')),
            ],
        ),
        migrations.CreateModel(
            name='Return_request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aldshop.users')),
            ],
        ),
        migrations.RemoveField(
            model_name='products',
            name='arrival_date',
        ),
        migrations.RemoveField(
            model_name='products',
            name='end_date',
        ),
    ]
