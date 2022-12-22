# Generated by Django 4.1.2 on 2022-11-18 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.CharField(default='buddy', max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('contact_number', models.CharField(max_length=50)),
                ('signup_day', models.CharField(default=18, max_length=50)),
                ('signup_month', models.CharField(default=11, max_length=50)),
                ('signup_year', models.CharField(default=2022, max_length=50)),
                ('active_status', models.CharField(default='active', max_length=50)),
                ('is_admin', models.CharField(default='false', max_length=50)),
                ('profile_image', models.ImageField(upload_to='profile_image/')),
                ('reference_id', models.CharField(default='0000000000', max_length=100)),
            ],
        ),
    ]