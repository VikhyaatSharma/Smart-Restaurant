# Generated by Django 4.1.3 on 2022-11-10 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('phno', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('doj', models.DateField()),
                ('address', models.TextField()),
            ],
        ),
    ]
