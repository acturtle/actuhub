# Generated by Django 5.1.5 on 2025-02-02 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('ec2_instance_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('private_key_path', models.CharField(blank=True, max_length=255)),
                ('username', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
