from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Category(models.Model):
    name=models.CharField(max_length=150,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_data=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return self.name
    

class Quantity(models.Model):
    name=models.CharField(max_length=100,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_data=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return self.name
    
class Foods(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField(null=True)
    image=models.ImageField(upload_to="foodsimages",default="default=jpg",null=True,blank=True)
    category_object=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="item")
    quantity_object=models.ManyToManyField(Quantity)
    price=models.PositiveIntegerField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_data=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return self.title
    


class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_data=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    @property
    def cart_item(self):
        return self.cartitem.filter(is_order_placed=False)
    
    @property
    def cart_item_count(self):
        return self.cart_item.count()
    

    @property

    def order_total(self):
        order_item=self.cart_item
        if order_item:
            total=sum([oi .item_total for oi in order_item])
            return total
        return 0



class OrderItem(models.Model):
    foods_object=models.ForeignKey(Foods,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField()
    basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_data=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_order_placed=models.BooleanField(default=False)

    @property
    def item_total(self):
        return self.qty*self.foods_object.price

  




def create_basket(sender,instance,created,**kwargs):
    if created:
        Basket.objects.create(owner=instance)

post_save.connect(create_basket,sender=User)            










