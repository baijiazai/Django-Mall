# Generated by Django 2.2.13 on 2020-06-20 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='书名')),
                ('img', models.ImageField(upload_to='book/%Y/%m/%d', verbose_name='图片')),
                ('book_class', models.CharField(choices=[('教育', '教育'), ('小说', '小说'), ('文艺', '文艺'), ('童书', '童书'), ('人文', '人文'), ('经营', '经营'), ('励志', '励志'), ('生活', '生活'), ('科技', '科技')], max_length=32, verbose_name='类别')),
                ('price', models.FloatField(default=0, verbose_name='价格')),
                ('scale', models.IntegerField(default=0, verbose_name='销量')),
                ('store', models.IntegerField(default=0, verbose_name='库存')),
                ('comments', models.IntegerField(default=0, verbose_name='评论数')),
                ('intro', models.TextField(blank=True, null=True, verbose_name='简介')),
            ],
            options={
                'verbose_name_plural': '书籍',
                'ordering': ['-scale', '-store', '-comments'],
            },
        ),
    ]
