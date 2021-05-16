# Generated by Django 3.1.7 on 2021-05-16 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.content')),
            ],
        ),
    ]
