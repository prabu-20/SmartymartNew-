import json
from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.http import HttpResponse
from shop.form import CustomUserForm
from django.contrib import messages
from .models import * 
from django.db.models import Q
import re
from django.contrib.auth import authenticate,login,logout

def HomePage(request):
    #products=Product.objects.filter(trending=1)
    #return render(request , 'index.html',{"products":products})
    render(request,"Working")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("/")

def login_page(request):
    if request.user.is_authenticated:
         return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect("home")
            else:
                messages.error(request,"Invalid User Name or Password")
                return render(request,"login.html")
    return render(request,"login.html")

def RegisterForm(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success you can Login Now....!")
            return redirect('/login')
    return render(request , 'register.html',{'form':form})

def Collections(request):
    category=Category.objects.filter(status=0)
    return render(request,'collections.html',{"category":category})

def WishList(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
   
        return render(request,'wish_list.html',{'fav':fav})
    else:
        return redirect("/")

def removefav(request,fid):
    favitem=Favourite.objects.get(id=fid)
    favitem.delete()
    return redirect("/wish_list")
    

def AddToCart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
   
        return render(request,'add_cart.html',{'cart':cart})
    else:
        return redirect("/")
    
def removecart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/add_cart")

def collectionview(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,'products\index.html',{"products":products,"category_name":name})
    else:
        messages.warning(request,"No Such Category Found")
        return redirect('collections')


def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)).exists:
        if(Product.objects.filter(name=pname,status=0)).exists:
            words=pname.split()
            product = Product.objects.filter(status=0)
            for word in words:
                product = product.filter(name__icontains=word)

                products = product.first
            return render(request,'products/products_details.html',{"products":products})
        else:
            messages.error(request,"No such Product Found")
            return redirect('collections')
    else:
        messages.error(request,"No Such Product Found")
        return redirect('collections')




def fav_page(request):
    if request.method=='POST':
    #if request.headers.get('x-requested-with')=='XMLHttpRequest':
      if request.user.is_authenticated:
        data=json.load(request)
        product_id=data['pid']
        product_status=Product.objects.get(id=product_id)
        if product_status:
            if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                return JsonResponse({'status':'Product Already In Wish List'},status=200)
            else:
                Favourite.objects.create(user=request.user,product_id=product_id)
                return JsonResponse({'status':'Product Added to Wish List'}, status=200)
      
      else:
        return JsonResponse({'status':'Login to Add Wish List'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def add_to_cart(request):
   # if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.method=='POST':
      if request.user.is_authenticated:
        data=json.load(request)
        product_qty=data['product_qty']
        product_id=data['pid']
        product_status=Product.objects.get(id=product_id)
        if product_status:
            if Cart.objects.filter(user=request.user.id,product_id=product_id):
                return JsonResponse({'status':'Product Already In Cart'},status=200)
            else:
                if product_status.quantity>=product_qty:
                    Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                    return JsonResponse({'status':'Product Added to Cart'},status=200)
                else:
                    return JsonResponse({'status':'Product Stock Not Available'},status=200)
        
      else:
        return JsonResponse({'status':'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)



def search_view(request):
    query = request.GET.get("q", "").lower()

    stop_words = [
        "i","need","want","show","me","give",
        "a","an","the","phone","mobile","please","list"
    ]

    words = re.findall(r'\w+', query)
    keywords = [w for w in words if w not in stop_words]

    price = re.findall(r'\d+', query)
    max_price = int(price[0]) if price else None

    is_best = "best" in query
    is_latest = "latest" in query

    #  START WITH ALL PRODUCTS
    products = Product.objects.all()

    #  MAIN SEARCH 
    if keywords:
        q_objects = Q()
        for word in keywords:
            q_objects |= Q(name__icontains=word)
            q_objects |= Q(description__icontains=word)
            q_objects |= Q(category__name__icontains=word)

        products = products.filter(q_objects)

    
    if not products.exists() and query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Price filter
    if max_price:
        products = products.filter(selling_price__lte=max_price)

    #  Sorting
    if is_best:
        products = products.order_by('-selling_price')
    elif is_latest:
        products = products.order_by('-id')

    context = {
        "products": products.distinct(),
        "query": query
    }

    return render(request, "search.html", context)  



