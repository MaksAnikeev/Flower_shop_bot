from django.contrib import admin
from django.utils.html import format_html

from .models import Reason, CategoryPrice, FlowersBunch, Order


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryPrice)
class CategoryPriceAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderPriceAdmin(admin.ModelAdmin):
    pass

@admin.register(FlowersBunch)
class FlowersBunchAdmin(admin.ModelAdmin):
    model = FlowersBunch
    list_display = ['name', 'preview', 'price']

    readonly_fields = ['preview']

    def preview(self, obj):
        if not obj.image:
            return 'нет картинки'
        return format_html('<img src="{url}" style="max-height: 100px;"/>',
                           url=obj.image.url)



