from django.db import models


BOOK_CLASS_LIST = [('教育', '教育'), ('小说', '小说'), ('文艺', '文艺'), ('童书', '童书'), ('人文', '人文'), ('经营', '经营'),
                   ('励志', '励志'), ('生活', '生活'), ('科技', '科技')]


class Book(models.Model):
    name = models.CharField(verbose_name='书名', max_length=200)
    img = models.ImageField(verbose_name='图片', upload_to='book/%Y/%m/%d')
    book_class = models.CharField(verbose_name='类别', max_length=32, choices=BOOK_CLASS_LIST)
    price = models.FloatField(verbose_name='价格', default=0)
    scale = models.IntegerField(verbose_name='销量', default=0)
    store = models.IntegerField(verbose_name='库存', default=0)
    comments = models.IntegerField(verbose_name='评论数', default=0)
    intro = models.TextField(verbose_name='简介', null=True, blank=True)

    class Meta:
        verbose_name_plural = '书籍'
        ordering = ['-scale', '-store', '-comments']



