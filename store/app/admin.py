from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(Varient)

admin.site.register(Orders)
admin.site.register(OrderItems)


admin.site.register(Wishlist)
class AdminModel(admin.ModelAdmin):
    list_display = ('varient', 'cart',  'quantity','price','id')
admin.site.register(CartItem, AdminModel)

class AdminModel(admin.ModelAdmin):
    list_display = ('user', 'name',  'address','pincode', 'phone', 'date')
admin.site.register(Shipping, AdminModel)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number', 'is_staff', 'is_superuser', 'is_active','is_anonymous')

admin.site.register(Users, UsersAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderid', 'user', 'items', 'total', 'date','orderitem')
    search_fields = ('orderid', 'user__email')
    list_filter = ('date',)



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shipping', 'date', 'quantity', 'price','is_completed')
    list_filter = ('date',)
    search_fields = ('user__username', 'varient__product__name')

