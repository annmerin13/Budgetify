# Generated by Django 5.1.6 on 2025-02-28 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_adminregistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_name', models.CharField(max_length=30)),
                ('admin_email', models.EmailField(max_length=30)),
                ('admin_password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_expensetype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expensetype_name', models.CharField(max_length=30)),
            ],
        ),
    ]
