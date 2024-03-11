# Generated by Django 5.0.2 on 2024-03-11 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('field', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=5000)),
                ('whatyouwilllearn', models.TextField(blank=True, max_length=10000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('price', models.CharField(max_length=10)),
                ('offerPrice', models.CharField(max_length=10)),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nameof_syllabus1', models.CharField(blank=True, max_length=200, null=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='syllabi', to='product.courses')),
            ],
        ),
        migrations.CreateModel(
            name='CourseData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(blank=True, max_length=200, null=True)),
                ('videourl', models.CharField(blank=True, max_length=1000, null=True)),
                ('codeType', models.CharField(blank=True, max_length=100, null=True)),
                ('note1', models.TextField(blank=True, max_length=100000, null=True)),
                ('code1', models.TextField(blank=True, max_length=100000, null=True)),
                ('note2', models.TextField(blank=True, max_length=100000, null=True)),
                ('code2', models.TextField(blank=True, max_length=100000, null=True)),
                ('note3', models.TextField(blank=True, max_length=100000, null=True)),
                ('code3', models.TextField(blank=True, max_length=100000, null=True)),
                ('duration_minutes', models.IntegerField(blank=True, null=True)),
                ('duration_seconds', models.IntegerField(blank=True, null=True)),
                ('content', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.syllabus')),
            ],
        ),
    ]