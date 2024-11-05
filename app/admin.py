from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . models import Cart, Customer, OrderPlaced, Payment, RecentlyViewed, Wishlist,product

# Register your models here.

@admin.register(product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [ 'id','title','discount_price','category','product_image']
    
@admin.register(Customer)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [ 'id','user','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','products','quantity']
    def products(self,obj):
        link = reverse( "admin:app_product_change",args =[obj.Product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.Product.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlaceModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status','payment']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display=['id','user','products']
    def products(self,obj):
        link = reverse( "admin:app_product_change",args =[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)

@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display=['id','user','products','viewed_at']
    def products(self,obj):
            link = reverse( "admin:app_product_change",args =[obj.Product.pk])
            return format_html('<a href="{}">{}</a>',link,obj.Product.title)
