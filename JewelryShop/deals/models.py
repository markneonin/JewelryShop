from django.db import models


class Gem(models.Model):
    """
    Камень
    """
    name = models.CharField(verbose_name='Название камня', max_length=4096, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Камень'
        verbose_name_plural = 'Камни'


class Customer(models.Model):
    """
    Клиент
    """
    name = models.CharField(verbose_name='Имя клиента', max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Deal(models.Model):
    """
    Сделка, fk - камень и клиент, каскадно не удаляется.
    """

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    gem = models.ForeignKey(Gem, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.customer.name} {self.gem.name} {self.amount}'

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'


