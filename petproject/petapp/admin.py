from django.contrib import admin
from .models import Pet,CartPet,Order

class PetAdmin(admin.ModelAdmin):
    list_display=("sid","name","color","price")
    
admin.site.register(Pet,PetAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=["pet","quantity","user"]

admin.site.register(CartPet,CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=["order_id","pet","quantity","user"]
    
admin.site.register(Order,OrderAdmin)
