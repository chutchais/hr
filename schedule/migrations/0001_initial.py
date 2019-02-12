# Generated by Django 2.0.4 on 2019-02-05 07:42

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkingCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_time', models.TimeField(blank=True)),
                ('end_time', models.TimeField(blank=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('color', colorfield.fields.ColorField(default='#CCFFFF', max_length=18)),
                ('dayoff', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='department.Section')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='workingcode',
            unique_together={('name', 'section')},
        ),
    ]