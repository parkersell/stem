# Generated by Django 3.0.4 on 2020-04-24 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='student/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_hr', models.IntegerField()),
                ('rec_sync', models.DateTimeField()),
                ('times_str_red', models.IntegerField()),
                ('time_rec_str_red', models.DateTimeField()),
                ('str_step_cor', models.IntegerField()),
                ('student_name', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, related_name='recent', to='datavis.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=30)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_referred', models.DateTimeField()),
                ('note', models.TextField(max_length=4000)),
                ('student_name', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='datavis.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peak_hr', models.IntegerField()),
                ('day_str_red', models.IntegerField()),
                ('str_step_cor', models.IntegerField()),
                ('student_name', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, related_name='day', to='datavis.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(unique=True)),
                ('min_hr', models.IntegerField()),
                ('min_steps', models.IntegerField()),
                ('student_name', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, related_name='chart', to='datavis.Student')),
            ],
        ),
    ]
