# Generated by Django 4.1 on 2023-01-21 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flower_shop', '0003_alter_flowersbunch_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bunch',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='flower_shop.flowersbunch', verbose_name='букет в заказе'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, default='', verbose_name='комментарий к заказу'),
        ),
        migrations.AlterField(
            model_name='order',
            name='lastname',
            field=models.CharField(blank=True, db_index=True, default='', max_length=50, verbose_name='Фамилия'),
        ),
    ]
