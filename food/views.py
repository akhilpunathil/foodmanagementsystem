from django.shortcuts import render,redirect

from django.views.generic import View,TemplateView

from food.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout

from django.contrib import messages
from food.models import Foods,OrderItem




class SignUpView(View):
    
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        return render(request,"login.html",{"form":form})
    

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()  
        return render(request,"login.html",{"form":form})  
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
           u_name=form.cleaned_data.get("username")
           pwd=form.cleaned_data.get("password")
           user_object=authenticate(request,username=u_name,password=pwd)
           if user_object:
               login(request,user_object)
               return redirect("index")
        messages.error(request,"invalidcredentials")    
        return render(request,"login.html",{"form":form})


class IndexView(View):
    def get(self,request,*args,**kwargs):

        qs=Foods.objects.all()
        return render(request,"index.html",{"data":qs})
    
class FoodsDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Foods.objects.get(id=id)
        return render(request,"foods_detail.html",{"data":qs}) 


class HomeView(TemplateView):
    template_name="base.html"


class AddToBasketView(View):
    def post(self,request,*args,**kwargs):
        qty=request.POST.get("qty")
        id=kwargs.get("pk")
        foods_obj=Foods.objects.get(id=id)
        OrderItem.objects.create(
            qty=qty,
            foods_object=foods_obj,
            basket_object=request.user.cart

        )
        return redirect("index")
    

class OrderItemListView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitem.filter(is_order_placed=False)
        return render(request,"cart_list.html",{"data":qs})  


class OrderItemRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        order_item_object=OrderItem.objects.get(id=id)
        order_item_object.delete()
        return redirect("order-items")     



class CartItemUpdateQuantityView(View):
    def post(self,request,*args,**kwargs):
        action=request.POST.get("counterbutton")
        print(action)
        id=kwargs.get("pk")
        order_item_object=OrderItem.objects.get(id=id)
        if action=="+":
            order_item_object.qty+=1
            order_item_object.save()
        else:
            order_item_object.qty-=1
            order_item_object.save()    
        return redirect("order-items")

