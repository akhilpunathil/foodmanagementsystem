from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Category(models.Model):
    name=models.CharField(max_length=150,unique=True)
    phone=models.CharField(max_length=12,null=True)
    restaurant=models.CharField(max_length=100,null=True)
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






class Bought(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    delivery_address=models.CharField(max_length=200)
    phone=models.CharField(max_length=12)
    email=models.CharField(max_length=200,null=True)
    is_paid=models.BooleanField(default=False)
    total=models.PositiveIntegerField()
    Bought_id=models.CharField(max_length=200,null=True)
    options=(
        ("cod","cod"),
        ("online","online")
    )

    payment=models.CharField(max_length=200,choices=options,default="cod")
    option=(
        ("order-placed","order-placed"),
        ("intransit","intransit"),
        ("dispatched","dispatched"),
        ("delivered","delivered"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=option,default="order-placed")  



    @property
    def get_bought_items(self):
        return self.purchaseitems.all()
    @property
    def get_bought_total(self):
        purchase_items=self.get_bought_items
        bought_total=0
        if purchase_items:
            bought_total=sum([pi.order_item_object.item_total for pi in purchase_items])
            return bought_total


class BoughtItems(models.Model):
    bought_object=models.ForeignKey(Bought,on_delete=models.CASCADE,related_name="purchaseitems")
    order_item_object=models.ForeignKey(OrderItem,on_delete=models.CASCADE)
   





