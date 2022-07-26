# Generated by Django 4.1 on 2022-08-10 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budget', '0004_budget_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetByYears',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_value', models.TextField(default='null')),
                ('year_number', models.TextField(default='null')),
                ('active', models.BooleanField()),
                ('field_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.budget')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetByMonths',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.TextField(default='null')),
                ('field_value', models.TextField(default='null')),
                ('month_number', models.TextField(default='null')),
                ('active', models.BooleanField()),
                ('field_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.budget')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
