# Generated by Django 3.1.6 on 2021-04-04 22:09

import django.core.serializers.json
from django.db import migrations

import eav.fields

try:
    from django.db.models import JSONField
except ImportError:
    from django_jsonfield_backport.models import JSONField


class Migration(migrations.Migration):
    dependencies = [
        ('eav', '0002_add_entity_ct_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='value_json',
            field=JSONField(
                blank=True,
                default=dict,
                encoder=django.core.serializers.json.DjangoJSONEncoder,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='datatype',
            field=eav.fields.EavDatatypeField(
                choices=[
                    ('text', 'Text'),
                    ('date', 'Date'),
                    ('float', 'Float'),
                    ('int', 'Integer'),
                    ('bool', 'True / False'),
                    ('object', 'Django Object'),
                    ('enum', 'Multiple Choice'),
                    ('json', 'JSON Object'),
                ],
                max_length=6,
                verbose_name='Data Type',
            ),
        ),
    ]
