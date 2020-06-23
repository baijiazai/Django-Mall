from django.db import models

BOOK_CLASS_LIST = [('教育', '教育'), ('小说', '小说'), ('文艺', '文艺'), ('童书', '童书'), ('人文', '人文'), ('经营', '经营'),
                   ('励志', '励志'), ('生活', '生活'), ('科技', '科技')]

ORDER_STATUS_LIST = [
    ('待付款', '待付款'), ('待发货', '待发货'), ('待收货', '待收货'), ('待评价', '待评价'), ('完结', '完结')
]


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


class User(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=200, unique=True)
    password = models.CharField(verbose_name='密码', max_length=256)
    email = models.EmailField(verbose_name='邮箱', max_length=200, unique=True)
    nickname = models.CharField(verbose_name='昵称', max_length=8)
    icon = models.ImageField(verbose_name='头像', upload_to='icon/%Y/%m/%d')

    class Meta:
        verbose_name_plural = '用户'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='书籍')
    count = models.IntegerField(verbose_name='数量', default=1)
    is_select = models.BooleanField(verbose_name='选中', default=True)

    class Meta:
        verbose_name_plural = '购物车'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    total = models.IntegerField(verbose_name='支付')
    time = models.DateTimeField(verbose_name='时间')
    status = models.CharField(verbose_name='状态', max_length=16, choices=ORDER_STATUS_LIST)

    class Meta:
        verbose_name_plural = '订单'


class OrderBook(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='书籍')
    count = models.IntegerField(verbose_name='数量', default=1)

    class Meta:
        verbose_name_plural = '订单书籍'
