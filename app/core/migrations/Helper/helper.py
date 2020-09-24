"""
Base Migration Module
"""
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_fields(name):
    """
    create fields in migration
    """
    return migrations.CreateModel(
        name=name,
        fields=[
            ('id',
             models.AutoField(auto_created=True, primary_key=True,
                              serialize=False,
                              verbose_name='ID')),
            ('name', models.CharField(max_length=255)),
            ('user',
             models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                               to=settings.AUTH_USER_MODEL)),
        ])
