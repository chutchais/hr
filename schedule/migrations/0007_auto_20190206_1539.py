# Generated by Django 2.1.5 on 2019-02-06 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20190206_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='working',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='working',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='working',
            name='status',
            field=models.CharField(choices=[('WORKING', 'On Working'), ('FINISH', 'Finished'), ('PRE_APPROVE', 'Pre-approved'), ('APPROVE', 'Approved'), ('ACCEPT', 'Accepted'), ('REJECT', 'Rejected'), ('COMPLETE', 'Completed')], default='WORKING', max_length=10),
        ),
    ]
