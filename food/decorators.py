from django.shortcuts import redirect
from food.models import OrderItem
from django.contrib import messages
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper    


def owner_permission_required(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        order_item=OrderItem.objects.get(id=id)
        if order_item.basket_object.owner !=request.user:
            messages.error(request,"permission denied")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper    

        







     