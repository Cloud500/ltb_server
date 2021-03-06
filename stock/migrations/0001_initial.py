# Generated by Django 3.2.9 on 2021-12-13 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ltb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_first_edition', models.BooleanField(verbose_name='Ist Erstausgabe')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quants', to='ltb.ltb')),
            ],
            options={
                'ordering': ['book', 'is_first_edition'],
                'permissions': [('add_quant_on_site', 'Can add Quants on the Site')],
            },
        ),
    ]
