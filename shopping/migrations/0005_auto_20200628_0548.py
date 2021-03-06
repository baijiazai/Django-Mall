# Generated by Django 2.2.13 on 2020-06-28 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0004_order_orderbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('待付款', '待付款'), ('待发货', '待发货'), ('待收货', '待收货'), ('待评价', '待评价'), ('完结', '完结')], max_length=16, verbose_name='状态'),
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.Book', verbose_name='书籍')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.User', verbose_name='用户')),
            ],
            options={
                'verbose_name_plural': '收藏',
            },
        ),
    ]
