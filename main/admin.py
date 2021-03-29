from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelForm
from django.utils.safestring import mark_safe

from .models import *


class ProductAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(f'<span style="color:red;"> Загружайте изображения с минимальным \
                                        требованием {Product.MIN_RESOLUTION}x{Product.MIN_RESOLUTION} </span>')
        self.fields['slug'].help_text = mark_safe(f'<span style="color:red;"> пишите в нижнем регистре\
                                        и без пробелов </span>')

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен превышать 3МБ! ')
        if img.height < Product.MIN_RESOLUTION or Product.MIN_RESOLUTION > img.width:
            raise ValidationError('Разрешение изображения меньше минимального!')
        if img.height > Product.MAX_RESOLUTION or Product.MAX_RESOLUTION < img.width:
            raise ValidationError('Разрешение изображения больше допустимого!')
        return image


class NotebookAdmin(admin.ModelAdmin):

    form = ProductAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebook'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    form = ProductAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(NoteBook, NotebookAdmin)
admin.site.register(SmartPhone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
