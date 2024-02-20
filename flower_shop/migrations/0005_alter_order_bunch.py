# Generated by Django 4.2.7 on 2024-01-06 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flower_shop', '0004_order_bunch_alter_order_comment_alter_order_lastname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='bunch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='flower_shop.flowersbunch', verbose_name='название букета в заказе'),
        ),
    ]
