from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('id','title','price','tags','brand','condition','state','date_created')
admin.site.register(ImageAdsModels)
admin.site.register(LastLogin)
admin.site.register(QrCode)
admin.site.register(Pricing)
admin.site.register(PaymentDetailsValues)
admin.site.register(WishlistData)
admin.site.register(CurrentDate)