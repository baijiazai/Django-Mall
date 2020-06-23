# Generated by Django 2.2.13 on 2020-06-23 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_auto_20200621_0338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(verbose_name='支付')),
                ('time', models.DateTimeField(verbose_name='时间')),
                ('status', models.CharField(choices=[('未付款', '未付款'), ('未发货', '未发货'), ('未收货', '未收货'), ('未评价', '未评价'), ('完结', '完结')], max_length=16, verbose_name='状态')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.User', verbose_name='用户')),
            ],
            options={
                'verbose_name_plural': '订单',
            },
        ),
        migrations.CreateModel(
            name='OrderBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='数量')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.Book', verbose_name='书籍')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.Order', verbose_name='订单')),
            ],
            options={
                'verbose_name_plural': '订单书籍',
            },
        ),
    ]
