# Generated by Django 3.2.8 on 2021-10-23 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0003_auto_20211023_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmessage',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat_app.groupmessage'),
        ),
        migrations.AlterField(
            model_name='singlechat',
            name='user_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='singlechat',
            name='user_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
