import razorpay
from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from food.forms import RegistrationForm,LoginForm
from food.models import Foods,OrderItem,Bought,BoughtItems
from food.decorators import signin_required,owner_permission_required 



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

@method_decorator([signin_required,never_cache],name="dispatch")
class IndexView(View):
    def get(self,request,*args,**kwargs):

        qs=Foods.objects.all()
        return render(request,"index.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")
class FoodsDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Foods.objects.get(id=id)
        return render(request,"foods_detail.html",{"data":qs}) 


class HomeView(TemplateView):
    template_name="base.html"

@method_decorator([signin_required,never_cache],name="dispatch")
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
    
@method_decorator([signin_required,never_cache],name="dispatch")
class OrderItemListView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitem.filter(is_order_placed=False)
        return render(request,"cart_list.html",{"data":qs})  

@method_decorator([signin_required,owner_permission_required,never_cache],name="dispatch")
class OrderItemRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        order_item_object=OrderItem.objects.get(id=id)
        order_item_object.delete()
        return redirect("order-items")     


@method_decorator([signin_required,owner_permission_required],name="dispatch")
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
    

@method_decorator([signin_required,never_cache],name="dispatch")
class CheckoutView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"checkout.html")
    
    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        payment_method=request.POST.get("payment")


        #creating bought_instance

        bought_obj=Bought.objects.create(
            user_object=request.user,
            delivery_address=address,
            phone=phone,
            email=email,
            total=request.user.cart.order_total,
            payment=payment_method

        )
        # creating boughtitems_instance

       


        try: 
            bought_items=request.user.cart.cart_item
            
            for oi in bought_items:
                BoughtItems.objects.create(
                   bought_object=bought_obj,
                   order_item_object=oi

                )
                oi.is_order_placed=True
                oi.save()
                print("text block 1")
 
        except:
            bought_obj.delete()

        finally:
            print("text block 2")
            print(payment_method)
            print(bought_obj)
            if payment_method=="online" and bought_obj:
                print("text block 3")
                client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

                data = { "amount": bought_obj.get_bought_total*100, "currency": "INR", "receipt": "order_rcptid_11" }
                payment = client.order.create(data=data) 
                print("payment initiate",payment)

            return redirect("index")  

@method_decorator([signin_required,never_cache],name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")    


class BoughtSummaryView(View):
    def get(self,request,*args,**kwargs):
        qs=Bought.objects.filter(user_object=request.user).exclude(status="cancelled")
        return render(request,"bought_summary.html",{"data":qs})
    


class BoughtItemRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        BoughtItems.objects.get(id=id).delete()
        return redirect("bought-summary")   
     




    


    


