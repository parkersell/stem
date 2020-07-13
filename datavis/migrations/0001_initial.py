# Generated by Django 3.0.4 on 2020-07-13 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Syncing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recent_synctime', models.DateTimeField()),
                ('sync_date', models.CharField(max_length=30)),
                ('student_name', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, related_name='syncing', to='datavis.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('min_hr', models.IntegerField()),
                ('min_steps', models.IntegerField(null=True)),
                ('student_name', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, related_name='chart', to='datavis.Student')),
            ],
        ),
    ]
