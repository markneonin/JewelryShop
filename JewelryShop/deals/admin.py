from django.urls import reverse
from django.utils.http import urlencode
from django.contrib import admin
from django.utils.html import format_html

from .models import *


@admin.register(Gem)
class GemAdmin(admin.ModelAdmin):
    """
    Добавляет в меню Gem столбец с каунтером-ссылкой на сделки по этому камню
    """

    list_display = ('name', 'view_deals_link')

    def view_deals_link(self, obj):
        count = obj.deal_set.count()
        url = (
                reverse('admin:deals_deal_changelist')
                + '?'
                + urlencode({'gem__id': f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Сделки</a>', url, count)

    view_deals_link.short_description = 'Сделки'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Добавляет в меню Customer столбец с каунтером-ссылкой на сделки этого клиента
    """
    list_display = ('name', 'view_deals_link')

    def view_deals_link(self, obj):
        count = obj.deal_set.count()
        url = (
                reverse('admin:deals_deal_changelist')
                + '?'
                + urlencode({'customer__id': f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Сделки</a>', url, count)

    view_deals_link.short_description = 'Сделки'


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    """
    Добавляет в меню Deal столбцы с ссылками на Gem и Customer
    """
    list_display = ('view_customer_link', 'view_gem_link', 'amount', 'quantity', 'date')

    def view_customer_link(self, obj):
        url = (
                reverse('admin:deals_customer_changelist')
                + '?'
                + urlencode({'deal__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, obj.customer.name)

    view_customer_link.short_description = 'Покупатель'

    def view_gem_link(self, obj):
        url = (
                reverse('admin:deals_gem_changelist')
                + '?'
                + urlencode({'deal__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, obj.gem.name)

    view_gem_link.short_description = 'Камень'

