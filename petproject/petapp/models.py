from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

# Create your models here.
class CustomManager(models.Manager):
    def get_price_range(self,p1,p2):
        return self.filter(price__range=(p1,p2))
    
    def cat_list(self):
        return self.filter(type__exact="Cat")
    
    def dog_list(self):
        return self.filter(type__exact="Dog")
    
class Pet(models.Model):
    t=(('Cat','Cat'),
       ('Dog','Dog'))
    sid=models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to="image/")
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=15,choices=t)
    color = models.CharField( max_length=30)
    age = models.IntegerField()
    location = models.CharField(max_length=50)
    desc = models.CharField( max_length=230)
    price = models.BigIntegerField()
    
    petss = CustomManager()
    objects = models.Manager()
    
    def petImg(self):
        return mark_safe(f"<img src='{self.image.url}' width='300px'>")
    
class CartPet(models.Model):
    pet = models.ForeignKey(Pet,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add = True)
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,default = 1)


class Order(models.Model):
    order_id = models.IntegerField()
    pet = models.ForeignKey(Pet,on_delete = models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete = models.CASCADE,default = 1)
    is_completed = models.BooleanField(default = False)