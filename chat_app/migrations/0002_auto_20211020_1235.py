# Generated by Django 3.2.8 on 2021-10-20 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmessage',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat_app.groupmessage'),
        ),
        migrations.AddField(
            model_name='singlechatmessage',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat_app.singlechatmessage'),
        ),
    ]
