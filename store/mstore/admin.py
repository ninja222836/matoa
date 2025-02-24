from django.contrib import admin
from django.utils.safestring import mark_safe

from mstore.models import *


class ImageAdmin(admin.StackedInline):
    model = ProductImage



class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'sell_price', 'is_published',
                    'time_create', 'category', 'related_product', 'get_html_photo', 'pid', 'card_image_webp', 'main_image_webp')

    prepopulated_fields = {"slug": ("name",)}

    fields = ('name', 'slug', 'price', 'discount', 'description', 'description_for_slider', 'is_published',
              'category', 'new', 'hit', 'model', 'related_product',
              'card_image', 'card_image_webp', 'main_image', 'main_image_webp')
    ordering = ('pid',)

    inlines = [ImageAdmin]

    def get_html_photo(self, object):
        if object.card_image:
            return mark_safe(f'<img src="{object.card_image.url}" width=50>')

    class Meta:
        model = Product



class ImageAdmin(admin.ModelAdmin):
    list_display = ('get_html_photo', 'product')

    def get_html_photo(self, object):
        if object.p_image:
            return mark_safe(f'<img src="{object.p_image.url}" width=50>')

    get_html_photo.short_description = 'photo'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    fields = ('name', 'slug')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ImageAdmin)
admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Testimonials)
admin.site.register(ProductScheme)
