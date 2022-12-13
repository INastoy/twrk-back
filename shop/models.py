from PIL import Image
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

        ordering = ['title']

    class StatusChoices(models.TextChoices):
        IN_STOCK = 'in stock', _('in stock')
        ON_ORDER = 'on order', _('on order')
        RECEIPT_EXPECTED = 'receipt expected', _('receipt expected')
        OUT_OF_STOCK = 'out of stock', _('out of stock')
        NOT_PRODUCED = 'not produced', _('not produced')

    title = models.CharField(_('title'), max_length=255)
    sku = models.CharField(_('sku'), max_length=255, unique=True)
    slug = models.SlugField(_('slug'), max_length=255)
    category = models.ForeignKey(verbose_name=_('category'), to='Category', on_delete=models.PROTECT,
                                 related_name='products')
    price = models.DecimalField(_('price'), max_digits=8, decimal_places=2)
    status = models.CharField(_('status'), max_length=255, choices=StatusChoices.choices,
                              default=StatusChoices.IN_STOCK)
    image = models.ImageField(_('image'), blank=True, upload_to='images/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])

    @staticmethod
    def convert_to_webp(source):
        img_format = source.rsplit('.')[-1]
        destination = source.replace(img_format, 'webp')

        image = Image.open(source)
        image.save(destination, format='webp')

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if self.image:
            self.convert_to_webp(self.image.name)

    def __str__(self):
        return self.title


class Category(models.Model):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

        ordering = ['title']

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)

    property_objects = models.ManyToManyField(verbose_name=_('properties'), to='PropertyObject')

    def __str__(self):
        return self.title


class PropertyObject(models.Model):
    class Meta:
        verbose_name = _('property object')
        verbose_name_plural = _('properties objects')

        ordering = ['title']

    class Type(models.TextChoices):
        STRING = 'string', _('string')
        DECIMAL = 'decimal', _('decimal')

    title = models.CharField(_('title'), max_length=255)
    code = models.SlugField(_('code'), max_length=255)
    value_type = models.CharField(_('value type'), max_length=10, choices=Type.choices)

    def __str__(self):
        return f'{self.title} ({self.get_value_type_display()})'


class PropertyValue(models.Model):
    class Meta:
        verbose_name = _('property value')
        verbose_name_plural = _('properties values')

        ordering = ['value_string', 'value_decimal']

    property_object = models.ForeignKey(to=PropertyObject, on_delete=models.PROTECT)

    value_string = models.CharField(_('value string'), max_length=255, blank=True, null=True)
    value_decimal = models.DecimalField(_('value decimal'), max_digits=11, decimal_places=2, blank=True, null=True)
    code = models.SlugField(_('code'), max_length=255)

    products = models.ManyToManyField(to=Product, related_name='properties')

    def __str__(self):
        return str(getattr(self, f'value_{self.property_object.value_type}', None))
