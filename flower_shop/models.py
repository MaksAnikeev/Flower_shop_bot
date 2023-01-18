from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField


class Reason(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Название повода',
    )

    class Meta:
        db_table = 'reason'
        verbose_name = 'повод'

        verbose_name_plural = 'поводы'

    def __str__(self):
        return f'{self.name}'


class CategoryPrice(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Категория цены',
    )

    class Meta:
        db_table = 'price'
        verbose_name = 'ценовая категория'

        verbose_name_plural = 'ценовые категории'

    def __str__(self):
        return f'{self.name}'


class FlowersBunch(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Название букета',
        blank=True,
        default=''
    )

    price = models.IntegerField(
        verbose_name='Цена букета'
    )

    image = models.ImageField(
        upload_to='flower_images',
        verbose_name='Картинка букета'
    )

    description = models.TextField(
        verbose_name='смысл букета'
    )

    composition = models.TextField(
        verbose_name='цветочный состав букета'
    )

    reason = models.ForeignKey(
        Reason,
        related_name='bunchs',
        verbose_name="повод для букета",
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        CategoryPrice,
        related_name='bunchs',
        verbose_name="ценовая категория",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'flower'
        verbose_name = 'букет'

        verbose_name_plural = 'букеты'

    def __str__(self):
        return f'{self.name}'



class Order(models.Model):
    NEW = 'raw_order'
    DONE = 'done'

    RIGHT_NOW = 'right_now'
    DELIVERY_CASH = 'delivery_pay_cash'
    INFO = 'check_to_manager'

    STATUS_ORDER = (
        (NEW, 'Необработанный'),
        (DONE, 'Выполнен'),
    )

    METHOD_PAYMENT = (
        (RIGHT_NOW, 'Электронно'),
        (DELIVERY_CASH, 'Наличностью при доставке'),
        (INFO, 'Уточнить у менеджера'),
    )

    firstname = models.CharField(
        verbose_name='Имя',
        max_length=50,
        db_index=True
    )

    lastname = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
        blank=True,
        db_index=True
    )

    address = models.CharField(
        max_length=100,
        verbose_name='адрес'
    )

    # phonenumber = PhoneNumberField(
    #     verbose_name='номер телефона',
    #     region='RU',
    #     db_index=True
    # )

    comment = models.TextField(
        verbose_name='комментарий к заказу',
        blank=True,
    )

    order_status = models.CharField(
        verbose_name='статус заказа',
        max_length=17,
        choices=STATUS_ORDER,
        default=NEW,
        db_index=True
        )

    method_payment = models.CharField(
        verbose_name='способ оплаты',
        max_length=17,
        choices=METHOD_PAYMENT,
        default=INFO,
        db_index=True
        )

    called_at = models.DateTimeField(
        verbose_name='дата звонка',
        null=True,
        blank=True,
        db_index=True
    )

    delivered_at = models.DateTimeField(
        verbose_name='дата доставки',
        db_index=True
    )


    class Meta:
        db_table = 'order'
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return self.firstname