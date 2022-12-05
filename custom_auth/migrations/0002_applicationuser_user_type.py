# Generated by Django 3.2 on 2022-12-02 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationuser',
            name='user_type',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Solution_provider', 'Solution_provider'), ('Solution_seeker', 'Solution_seeker')], default='Admin', max_length=40),
        ),
    ]