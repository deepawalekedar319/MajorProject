from itertools import product
from statistics import quantiles
from unicodedata import category
from django.shortcuts import render,redirect
from django.views import View
from .models import BookedCart, BusCart, BusDetail, Customer, FlightCart, FlightDetail, HomeServices, HotelRooms, Movie,  Product, Cart, OrderPlaced, RoomsCart, ServicesCart, TrainBooked, TrainDetail
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        totalitem=0
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        laptops=Product.objects.filter(category='L')
        bangles=Product.objects.filter(category='BJ')
        keyboard=Product.objects.filter(category='KB')
        printer=Product.objects.filter(category='PE')
        drives=Product.objects.filter(category='PD')
        fridge=Product.objects.filter(category='FD')
        cooler=Product.objects.filter(category='CL')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'totalitem':totalitem,
            'bangles':bangles,'laptops':laptops,'keyboard':keyboard,'printers':printer,'drives':drives,
            'cooler':cooler, 'fridge':fridge
        })
 
class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            item_already_in_cart= Cart.objects.filter(Q(product=product.id) & Q(user= request.user)).exists()

        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user = user, product = product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})    
        else:
            return render(request,'app/emptycart.html')    


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity':c.quantity,
            'amount':amount,
           'totalamount':amount + shipping_amount
        }   
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
        data = {
           'quantity':c.quantity,
           'amount':amount,
           'totalamount':amount + shipping_amount
        }   
        return JsonResponse(data)            

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
        data = {
           'amount':amount,
           'totalamount':amount + shipping_amount
        }   
        return JsonResponse(data)            


# def buy_now(request):
#  return render(request, 'app/buynow.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user = usr, name=name, locality = locality, city = city, state = state,zipcode = zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})    

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})


# All Electronics
def mobile(request, data=None):
    mobiles=None
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data== 'Realme' or data=='Samsung' or data== 'REDMI' or data=='Apple':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price_Lt=10000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price_gt=10000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def cooler_view(request, data=None):
    mobiles=None
    if data==None:
        mobiles=Product.objects.filter(category='CL')
    elif data== 'Singer' or data=='Bajaj' or data== 'Usha' or data=='Hindware':
        mobiles=Product.objects.filter(category='CL').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='CL').filter(discounted_price_Lt=10000)
    elif data=='above':
        mobiles=Product.objects.filter(category='CL').filter(discounted_price_gt=10000)
    return render(request, 'app/coolers.html',{'allCycles':mobiles})    

def laptops_view(request, data=None):
    allLatops = None
    if data==None:
        allLatops = Product.objects.filter(category='L')
    elif data== 'Apple' or data=='Lenovo' or data== 'Dell' or data== 'Mi':
        allLatops=Product.objects.filter(category='L').filter(brand=data)
    elif data=='below':
        allLatops=Product.objects.filter(category='L').filter(discounted_price__lte=10000)
    elif data=='above':
        allLatops=Product.objects.filter(category='L').filter(discounted_price__gte=10000)  
    return render(request,'app/laptops.html',{'allCycles':allLatops})   

def monitors_view(request, data=None):
    allLatops = None
    if data==None:
        allLatops = Product.objects.filter(category='monitors')
    elif data== 'Decdeal' or data=='Lenovo':
        allLatops=Product.objects.filter(category='monitors').filter(brand=data)
    elif data=='below':
        allLatops=Product.objects.filter(category='monitors').filter(discounted_price__lte=10000)
    elif data=='above':
        allLatops=Product.objects.filter(category='monitors').filter(discounted_price__gte=10000)  
    return render(request,'app/monitors.html',{'allCycles':allLatops})

def computers_view(request, data=None):
    allLatops = None
    if data==None:
        allLatops = Product.objects.filter(category='computers')
    elif data== 'Dell' or data=='Lenovo':
        allLatops=Product.objects.filter(category='computers').filter(brand=data)
    elif data=='below':
        allLatops=Product.objects.filter(category='computers').filter(discounted_price__lte=10000)
    elif data=='above':
        allLatops=Product.objects.filter(category='computers').filter(discounted_price__gte=10000)  
    return render(request,'app/computers.html',{'allCycles':allLatops})

def AC_view(request, data=None):
    allLatops = None
    if data==None:
        allLatops = Product.objects.filter(category='ACs')
    elif data== 'CROMA' or data=='Lloyd':
        allLatops=Product.objects.filter(category='ACs').filter(brand=data)
    elif data=='below':
        allLatops=Product.objects.filter(category='ACs').filter(discounted_price__lte=10000)
    elif data=='above':
        allLatops=Product.objects.filter(category='ACs').filter(discounted_price__gte=10000)  
    return render(request,'app/ac.html',{'allCycles':allLatops})

def Fridge_view(request, data=None):
    allLatops = None
    if data==None:
        allLatops = Product.objects.filter(category='FD')
    elif data== 'LG' or data=='Godrej' or data=='Samsung':
        allLatops=Product.objects.filter(category='FD').filter(brand=data)
    elif data=='below':
        allLatops=Product.objects.filter(category='FD').filter(discounted_price__lte=10000)
    elif data=='above':
        allLatops=Product.objects.filter(category='FD').filter(discounted_price__gte=10000)  
    return render(request,'app/fridge.html',{'allCycles':allLatops})


def printers_view(request, data=None):
    allLatops = None
    if data==None:
        allLatops = Product.objects.filter(category='printers')
    elif data== 'Canon' or data=='Lenovo':
        allLatops=Product.objects.filter(category='printers').filter(brand=data)
    elif data=='below':
        allLatops=Product.objects.filter(category='printers').filter(discounted_price__lte=10000)
    elif data=='above':
        allLatops=Product.objects.filter(category='printers').filter(discounted_price__gte=10000)  
    return render(request,'app/printers.html',{'allCycles':allLatops})

def speckers_view(request, data=None):
    allLatops = None
    if data==None:
        allLatops = Product.objects.filter(category='speakers')
    elif data== 'AmazonBasics' or data=='INSTAPLAY':
        allLatops=Product.objects.filter(category='speakers').filter(brand=data)
    elif data=='below':
        allLatops=Product.objects.filter(category='speakers').filter(discounted_price__lte=10000)
    elif data=='above':
        allLatops=Product.objects.filter(category='speakers').filter(discounted_price__gte=10000)  
    return render(request,'app/speakers.html',{'allCycles':allLatops})    

# def login(request):
#  return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})    

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount' : totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer = customer, product=c.product,quantity = c.quantity).save()
        c.delete()
    return redirect("orders")    

# Alla Toys
def bicycle_view(request, data=None):
    allCycles = None
    if data==None:
        allCycles = Product.objects.filter(category='BC')
    elif data== 'Hero' or data=='SpeedBird' or data== 'Beetle':
        allCycles=Product.objects.filter(category='BC').filter(brand=data)
    elif data=='below':
        allCycles=Product.objects.filter(category='BC').filter(discounted_price__lte=1000)
    elif data=='above':
        allCycles=Product.objects.filter(category='BC').filter(discounted_price__gte=1000)
    return render(request,'app/bicycle.html',{'allCycles':allCycles})

def trains_view(request, data=None):
    allTrains = None
    if data==None:
        allTrains = Product.objects.filter(category='TT')
    elif data== 'ClassicGlow' or data=='WoodTrains' or data== 'CATRON':
        allTrains=Product.objects.filter(category='TT').filter(brand=data)
    elif data=='below':
        allTrains=Product.objects.filter(category='TT').filter(discounted_price__lte=1000)
    elif data=='above':
        allTrains=Product.objects.filter(category='TT').filter(discounted_price__gte=1000)  
    return render(request,'app/trains.html',{'allCycles':allTrains})   

def dolls_view(request, data=None):
    allDolls = None
    if data==None:
        allDolls = Product.objects.filter(category='BT')
    elif data== 'SCOOBA' or data=='Barbie':
        allDolls=Product.objects.filter(category='BT').filter(brand=data)
    elif data=='below':
        allDolls=Product.objects.filter(category='BT').filter(discounted_price__lte=1000)
    elif data=='above':
        allDolls=Product.objects.filter(category='BT').filter(discounted_price__gte=1000)  
    return render(request,'app/barbie.html',{'allCycles':allDolls})   

def bear_view(request, data=None):
    allBears = None
    if data==None:
        allBears = Product.objects.filter(category='TB')
    elif data== 'ZIRAAT' or data=='TEDSTREE' or data=='Toytales' or data=='BACKBANCHERS':
        allBears=Product.objects.filter(category='TB').filter(brand=data)
    elif data=='below':
        allBears=Product.objects.filter(category='TB').filter(discounted_price__lte=1000)
    elif data=='above':
        allBears=Product.objects.filter(category='TB').filter(discounted_price__gte=1000)  
    return render(request,'app/bear.html',{'allCycles':allBears})       

def plain_view(request, data=None):
    allPlain = None
    if data==None:
        allPlain = Product.objects.filter(category='PT')
    elif data== 'KiddyBuddy' or data=='Toyshine' or data== 'ClassicGlow' or data=='CATRON':
        allPlain=Product.objects.filter(category='PT').filter(brand=data)
    elif data=='below':
        allPlain=Product.objects.filter(category='PT').filter(discounted_price__lte=1000)
    elif data=='above':
        allPlain=Product.objects.filter(category='PT').filter(discounted_price__gte=1000)  
    return render(request,'app/plain.html',{'allCycles':allPlain})   

# Jewellary 
def bangles_view(request, data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='BJ')
    elif data== 'KARATCART' or data=='Rijoli' or data== 'PEORA':
        allBangles=Product.objects.filter(category='BJ').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='BJ').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='BJ').filter(discounted_price__gte=1000)  
    return render(request,'app/bangles.html',{'allCycles':allBangles}) 

def earRings_view(request, data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='RJ')
    elif data== 'VoyllaPerfect' or data=='Royals' or data=='KARATCART':
        allBangles=Product.objects.filter(category='RJ').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='RJ').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='RJ').filter(discounted_price__gte=1000)  
    return render(request,'app/rings.html',{'allCycles':allBangles})     


def rings_view(request, data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='EJ')
    elif data== 'VoyllaPerfect' or data=='SwastiJewels':
        allBangles=Product.objects.filter(category='EJ').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='EJ').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='EJ').filter(discounted_price__gte=1000)  
    return render(request,'app/earrings.html',{'allCycles':allBangles})         

def bracelate_view(request, data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='JB')
    elif data== 'YouBell' or data=='CrystalHeaven':
        allBangles=Product.objects.filter(category='JB').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='JB').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='JB').filter(discounted_price__gte=1000)  
    return render(request,'app/bracelets.html',{'allCycles':allBangles})     

def necklace_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='NJ')
    elif data== 'REEVA' or data=='JewelMaze' or data == 'Sukkhi':
        allBangles=Product.objects.filter(category='NJ').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='NJ').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='NJ').filter(discounted_price__gte=1000)  
    return render(request,'app/necklace.html',{'allCycles':allBangles})

def broochs_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='BR')
    elif data== 'HASHBURYS' or data=='SANNIDHI' or data == 'OmJewells' or data=='Okos':
        allBangles=Product.objects.filter(category='BR').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='BR').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='BR').filter(discounted_price__gte=1000)  
    return render(request,'app/brooches.html',{'allCycles':allBangles})


def nosepin_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='NP')
    elif data== 'IJewels' or data=='KYOOTJEWELS':
        allBangles=Product.objects.filter(category='NP').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='NP').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='NP').filter(discounted_price__gte=1000)  
    return render(request,'app/nosepin.html',{'allCycles':allBangles})    

def bellypin_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='BPP')
    elif data== 'Buckle':
        allBangles=Product.objects.filter(category='BPP').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='BPP').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='BPP').filter(discounted_price__gte=1000)  
    return render(request,'app/bellychains.html',{'allCycles':allBangles})    

def chains_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='JCH')
    elif data== 'BradoJewelery' or data=='MINUTIAE' or data == 'Jixara':
        allBangles=Product.objects.filter(category='JCH').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='JCH').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='JCH').filter(discounted_price__gte=1000)  
    return render(request,'app/brooches.html',{'allCycles':allBangles})            

def sarees_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='SSS')
    elif data== 'AdrikaSensationalSarees' or data=='BanarasiSilk' or data == 'PEDDINGPATTAFENTA':
        allBangles=Product.objects.filter(category='SSS').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='SSS').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='SSS').filter(discounted_price__gte=1000)  
    return render(request,'app/sarees.html',{'allCycles':allBangles})            


def kurtis_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='KTS')
    elif data== 'Embroideredflaredkurti' or data=='JollyMorpichKurti' or data == 'GeorgetteKurtis':
        allBangles=Product.objects.filter(category='KTS').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='KTS').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='KTS').filter(discounted_price__gte=1000)  
    return render(request,'app/kurtis.html',{'allCycles':allBangles})            


def western_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='WSS')
    elif data== 'UrbaneGraceful' or data=='TrendySensational' or data == 'ClassicFashionista':
        allBangles=Product.objects.filter(category='WSS').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='WSS').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='WSS').filter(discounted_price__gte=1000)  
    return render(request,'app/western.html',{'allCycles':allBangles})   

def suits_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='STS')
    elif data== 'AagamAlluringWomen' or data=='ChitrarekhaGraceful' or data == 'PRANJULCOTTONDUPATTASET':
        allBangles=Product.objects.filter(category='STS').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='STS').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='STS').filter(discounted_price__gte=1000)  
    return render(request,'app/suits.html',{'allCycles':allBangles})    

def ethinic_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='ETS')
    elif data== 'Lehenga' or data=='KashviDrishya' or data == 'AishaniDrishya':
        allBangles=Product.objects.filter(category='ETS').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='ETS').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='ETS').filter(discounted_price__gte=1000)  
    return render(request,'app/ethinic.html',{'allCycles':allBangles})           

def womenAss_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='PUS')
    elif data=='below':
        allBangles=Product.objects.filter(category='PUS').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='PUS').filter(discounted_price__gte=1000)  
    return render(request,'app/womenAss.html',{'allCycles':allBangles})     

def menTshirt_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='TTS')
    elif data== 'UrbaneElegant' or data=='Smartness' or data == 'ClassicGraceful':
        allBangles=Product.objects.filter(category='TTS').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='TTS').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='TTS').filter(discounted_price__gte=1000)  
    return render(request,'app/Tshirts.html',{'allCycles':allBangles})   

def menshirt_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='SST')
    elif data== 'UrbaneSensational' or data=='ClassicSensational' or data == 'PrettyFashionate':
        allBangles=Product.objects.filter(category='SST').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='SST').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='SST').filter(discounted_price__gte=1000)  
    return render(request,'app/shirts.html',{'allCycles':allBangles})                       

def jeans_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='JNS')
    elif data== 'CasualTrendy' or data=='FancyFashionista' or data == 'RavishingModern':
        allBangles=Product.objects.filter(category='JNS').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='JNS').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='JNS').filter(discounted_price__gte=1000)  
    return render(request,'app/jeans.html',{'allCycles':allBangles})                       


def nightWear_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='NTS')
    elif data== 'VimalJonney' or data=='ComfyFabulous':
        allBangles=Product.objects.filter(category='NTS').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='NTS').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='NTS').filter(discounted_price__gte=1000)  
    return render(request,'app/nightWear.html',{'allCycles':allBangles})                       


def partyWear_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='PTW')
    elif data== 'UniqueMen' or data=='ElegantMen' or data == 'ClassicMen':
        allBangles=Product.objects.filter(category='PTW').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='PTW').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='PTW').filter(discounted_price__gte=1000)  
    return render(request,'app/partyWear.html',{'allCycles':allBangles})                       


def mesAss_view(request, data = None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='ACC')
    elif data=='below':
        allBangles=Product.objects.filter(category='ACC').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='ACC').filter(discounted_price__gte=1000)  
    return render(request,'app/menAss.html',{'allCycles':allBangles})                       


# Grocery
def grocery_counter(request, data = None):
    allItems = None
    if data==None:
        allItems = Product.objects.filter(Q(category='FTS')| Q(category='SKS') | 
        Q(category='OIL') | Q(category='MET') | Q(category='FSH') | Q(category='BVS') | 
        Q(category='VTS') | Q(category='MSL') | Q(category='EGG') | Q(category='FGS'))
    elif data=='FTS':
        allItems=Product.objects.filter(category='FTS') 
    elif data=='SKS':
        allItems=Product.objects.filter(category='SKS') 
    elif data=='OIL':
        allItems=Product.objects.filter(category='OIL') 
    elif data=='MET':
        allItems=Product.objects.filter(category='MET') 
    elif data=='FSH':
        allItems=Product.objects.filter(category='FSH') 
    elif data=='BVS':
        allItems=Product.objects.filter(category='BVS') 
    elif data=='MSL':
        allItems=Product.objects.filter(category='MSL') 
    elif data=='EGG':
        allItems=Product.objects.filter(category='EGG') 
    elif data=='FGS':
        allItems=Product.objects.filter(category='FGS') 
    elif data=='VTS':
        allItems=Product.objects.filter(category='VTS') 
    return render(request,'app/grocery.html',{'allCycles':allItems}) 


def houseApplience_view(request, data = None):
    allItems = None
    if data==None:
        allItems = Product.objects.filter(Q(category='Stoves')| Q(category='LightBulbs') | 
        Q(category='Ovens') | Q(category='Mixers') | Q(category='Blenders') | Q(category='Fans') | 
        Q(category='WashineMachines') | Q(category='VaccumCleaners') | Q(category='RiceCookers') | Q(category='PressureCookers')
        | Q(category='WaterPurifiers'))
    elif data=='Stoves':
        allItems=Product.objects.filter(category='Stoves') 
    elif data=='VaccumCleaners':
        allItems=Product.objects.filter(category='VaccumCleaners') 
    elif data=='LightBulbs':
        allItems=Product.objects.filter(category='LightBulbs') 
    elif data=='Ovens':
        allItems=Product.objects.filter(category='Ovens') 
    elif data=='Mixers':
        allItems=Product.objects.filter(category='Mixers') 
    elif data=='Blenders':
        allItems=Product.objects.filter(category='Blenders') 
    elif data=='Fans':
        allItems=Product.objects.filter(category='Fans') 
    elif data=='WashineMachines':
        allItems=Product.objects.filter(category='WashineMachines') 
    elif data=='RiceCookers':
        allItems=Product.objects.filter(category='RiceCookers') 
    elif data=='PressureCookers':
        allItems=Product.objects.filter(category='PressureCookers') 
    elif data=='WaterPurifiers':
        allItems=Product.objects.filter(category='WaterPurifiers') 
    return render(request,'app/houseapplience.html',{'allCycles':allItems}) 

def furtinures_View(request, data = None):
    allItems = None
    if data==None:
        allItems = Product.objects.filter(Q(category='Beds')| Q(category='SofaSets') | 
        Q(category='Cupboards') | Q(category='BookCases') | Q(category='Tables') | Q(category='ArmChair'))
    elif data=='Beds':
        allItems=Product.objects.filter(category='Beds') 
    elif data=='SofaSets':
        allItems=Product.objects.filter(category='SofaSets') 
    elif data=='Cupboards':
        allItems=Product.objects.filter(category='Cupboards') 
    elif data=='BookCases':
        allItems=Product.objects.filter(category='BookCases') 
    elif data=='Tables':
        allItems=Product.objects.filter(category='Tables') 
    elif data=='ArmChair':
        allItems=Product.objects.filter(category='ArmChair') 
    return render(request,'app/furtinures.html',{'allCycles':allItems}) 

def gym_view(request, data = None):
    allItems = None
    if data==None:
        allItems = Product.objects.filter(Q(category='GSD')| Q(category='GCP') | 
        Q(category='GLM') | Q(category='GTM') | Q(category='GBM') | Q(category='GLP') | 
        Q(category='GAM') | Q(category='GDM') | Q(category='GRS') | Q(category='Bars')
        | Q(category='GALM'))
    elif data=='GALM':
        allItems=Product.objects.filter(category='GALM') 
    elif data=='Bars':
        allItems=Product.objects.filter(category='Bars') 
    elif data=='GAM':
        allItems=Product.objects.filter(category='GAM') 
    elif data=='GDM':
        allItems=Product.objects.filter(category='GDM') 
    elif data=='GRS':
        allItems=Product.objects.filter(category='GRS') 
    elif data=='GLP':
        allItems=Product.objects.filter(category='GLP') 
    elif data=='GBM':
        allItems=Product.objects.filter(category='GBM') 
    elif data=='GTM':
        allItems=Product.objects.filter(category='GTM') 
    elif data=='GLM':
        allItems=Product.objects.filter(category='GLM') 
    elif data=='GCP':
        allItems=Product.objects.filter(category='GCP') 
    elif data=='GSD':
        allItems=Product.objects.filter(category='GSD') 
    return render(request,'app/gym.html',{'allCycles':allItems}) 

def corns_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Corns')
    elif data== 'PrivateLabel' or data=='4700BCPopcorn':
        allBangles=Product.objects.filter(category='Corns').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Corns').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Corns').filter(discounted_price__gte=1000)  
    return render(request,'app/corns.html',{'allCycles':allBangles})   

def gas_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Gasoline')
    elif data== 'Motul' or data=='Shell':
        allBangles=Product.objects.filter(category='Gasoline').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Gasoline').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Gasoline').filter(discounted_price__gte=1000)  
    return render(request,'app/gas.html',{'allCycles':allBangles}) 

def lumber_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Lumber')
    elif data=='BarringtonHardwoods':
        allBangles=Product.objects.filter(category='Lumber').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Lumber').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Lumber').filter(discounted_price__gte=1000)  
    return render(request,'app/lumber.html',{'allCycles':allBangles}) 

def plastic_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Plastic')
    elif data== 'Chetan' or data=='K2':
        allBangles=Product.objects.filter(category='Plastic').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Plastic').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Plastic').filter(discounted_price__gte=1000)  
    return render(request,'app/plastic.html',{'allCycles':allBangles})       

def forest_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Forest')
    elif data== 'ParleRopvatika' or data=='SKYFUN':
        allBangles=Product.objects.filter(category='Forest').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Forest').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Forest').filter(discounted_price__gte=1000)  
    return render(request,'app/forest.html',{'allCycles':allBangles})      

def mineral_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Mineral')
    elif data== 'Santevia' or data=='ThamesAnsKosmos':
        allBangles=Product.objects.filter(category='Mineral').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Mineral').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Mineral').filter(discounted_price__gte=1000)  
    return render(request,'app/mineral.html',{'allCycles':allBangles})      

def natural_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Forest')
    elif data== 'ParleRopvatika' or data=='SKYFUN':
        allBangles=Product.objects.filter(category='Forest').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Forest').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Forest').filter(discounted_price__gte=1000)  
    return render(request,'app/natural.html',{'allCycles':allBangles})      

def coal_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Coal')
    elif data== 'Koyla' or data=='BiharOrganicCharcoal':
        allBangles=Product.objects.filter(category='Coal').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Coal').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Coal').filter(discounted_price__gte=1000)  
    return render(request,'app/coal.html',{'allCycles':allBangles})      

def steel_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Steel')
    elif data== 'RamaSteel' or data=='AlphaSteels':
        allBangles=Product.objects.filter(category='Steel').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Steel').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Steel').filter(discounted_price__gte=1000)  
    return render(request,'app/steel.html',{'allCycles':allBangles})      


def bandages_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Bandages')
    elif data== 'ChitraMedical' or data=='Apollo':
        allBangles=Product.objects.filter(category='Bandages').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Bandages').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Bandages').filter(discounted_price__gte=1000)  
    return render(request,'app/bandages.html',{'allCycles':allBangles})      

def injection_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Injections')
    elif data=='Pmw':
        allBangles=Product.objects.filter(category='Injections').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Injections').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Injections').filter(discounted_price__gte=1000)  
    return render(request,'app/injection.html',{'allCycles':allBangles})      

def drops_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Drops')
    elif data== 'Cipla' or data=='Himalaya':
        allBangles=Product.objects.filter(category='Drops').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Drops').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Drops').filter(discounted_price__gte=1000)  
    return render(request,'app/drops.html',{'allCycles':allBangles})      

def ointments_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Ointments')
    elif data== 'TigerBalm' or data=='Charak':
        allBangles=Product.objects.filter(category='Ointments').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Ointments').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Ointments').filter(discounted_price__gte=1000)  
    return render(request,'app/ointments.html',{'allCycles':allBangles})      

def tablets_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Tablets')
    elif data== 'Fortis' or data=='Cipla':
        allBangles=Product.objects.filter(category='Tablets').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Tablets').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Tablets').filter(discounted_price__gte=1000)  
    return render(request,'app/tablets.html',{'allCycles':allBangles})      

def syrups_view(request,data=None):
    allBangles = None
    if data==None:
        allBangles = Product.objects.filter(category='Syrups')
    elif data== 'Himalaya' or data=='UjwalaAyurvedashram':
        allBangles=Product.objects.filter(category='Syrups').filter(brand=data)
    elif data=='below':
        allBangles=Product.objects.filter(category='Syrups').filter(discounted_price__lte=1000)
    elif data=='above':
        allBangles=Product.objects.filter(category='Syrups').filter(discounted_price__gte=1000)  
    return render(request,'app/syrups.html',{'allCycles':allBangles})      


# Food Court
def food_counter(request, data = None):
    allItems = None
    if data==None:
        allItems = Product.objects.filter(Q(category='BRR')| Q(category='PZZ') | 
        Q(category='CHH') | Q(category='DSS') | Q(category='MSS') | Q(category='TFS'))
    elif data=='BRR':
        allItems=Product.objects.filter(category='BRR') 
    elif data=='PZZ':
        allItems=Product.objects.filter(category='PZZ') 
    elif data=='CHH':
        allItems=Product.objects.filter(category='CHH') 
    elif data=='DSS':
        allItems=Product.objects.filter(category='DSS') 
    elif data=='MSS':
        allItems=Product.objects.filter(category='MSS') 
    elif data=='TFS':
        allItems=Product.objects.filter(category='TFS') 
    return render(request,'app/food.html',{'allCycles':allItems}) 

# Hotel Tickets Booking
def hotel_booking(request,data = None):
    allRooms = HotelRooms.objects.all()
    if data=='single':
        allRooms = HotelRooms.objects.filter(category='single')
    elif data=='double':
        allRooms = HotelRooms.objects.filter(category='double')
    elif data=='deluex':
        allRooms = HotelRooms.objects.filter(category='5 Star Deluex')
    elif data=='family':
        allRooms = HotelRooms.objects.filter(category='Family Type Room')
    elif data=='studio':
        allRooms = HotelRooms.objects.filter(category='Studio Room')
    return render(request,'app/hotel.html',{'allCycles':allRooms})

def hotel_service_view(request,pk):
    totalitem=0
    product=HotelRooms.objects.get(pk=pk)
    if request.method=='POST':        
        user = request.user
        product_id = request.POST.get('prod_id')
        service = HotelRooms.objects.get(id=product_id)
        date = request.POST.get('date')
        days = request.POST.get('days')
        RoomsCart(user = user, services = service,date = date, days = days).save()
        return redirect('/hotel-cart')
    # item_already_in_cart=False
    # if request.user.is aunthenticated:
    #     totalitem=len(Cart.objects.filter(user=request.user))
    #     item_already_in_cart=cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/hoteldetails.html', {'product':product})#, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

def rooms_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = RoomsCart.objects.filter(user=user)
        cart_product = [p for p in RoomsCart.objects.all() if p.user==user]
        if cart_product:
            return render(request,'app/roomsaddtocart.html',{'carts':cart})   
        else:
            return render(request,'app/emptyroom.html')    


def room_delete_service(request,pk):
    c = RoomsCart.objects.get(Q(id=pk) & Q(user=request.user))    
    c.delete()
    return redirect('/hotel-cart')

# Home Services
def home_services(request,data=None):
    allServices = HomeServices.objects.all()
    if data=='Plumber':
        allServices = HomeServices.objects.filter(category='Plumber')
    elif data=='Electrician':
        allServices = HomeServices.objects.filter(category='Electrician')
    elif data=='Carpentry':    
        allServices = HomeServices.objects.filter(category='Carpentry')
    elif data=='Carpentry':    
        allServices = HomeServices.objects.filter(category='Carpentry')
    elif data=='Welder':    
        allServices = HomeServices.objects.filter(category='Welder')
    elif data=='Saloon':    
        allServices = HomeServices.objects.filter(category='Saloon')
    elif data=='Tailor':    
        allServices = HomeServices.objects.filter(category='Tailor')
    return render(request,'app/homeservices.html',{'allCycles':allServices})

@login_required
def ServicesDetailsView(request,pk):
    totalitem=0
    product=HomeServices.objects.get(pk=pk)
    if request.method=='POST':        
        user = request.user
        product_id = request.POST.get('prod_id')
        service = HomeServices.objects.get(id=product_id)
        date = request.POST.get('date')
        days = request.POST.get('days')
        hours = request.POST.get('hours')
        ServicesCart(user = user, services = service,date = date, days = days, hours = hours).save()
        return redirect('/services-cart')
    # item_already_in_cart=False
    # if request.user.is aunthenticated:
    #     totalitem=len(Cart.objects.filter(user=request.user))
    #     item_already_in_cart=cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/servicesdetails.html', {'product':product})#, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})


@login_required
def service_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = ServicesCart.objects.filter(user=user)
        cart_product = [p for p in ServicesCart.objects.all() if p.user==user]
        if cart_product:
            return render(request,'app/servicesaddtocart.html',{'carts':cart})   
        else:
            return render(request,'app/emptyservice.html')    

@login_required
def delete_service(request,pk):
    c = ServicesCart.objects.get(Q(id=pk) & Q(user=request.user))    
    c.delete()
    return redirect('/services-cart')


# Railways
def railway_view(request):
    trains = TrainDetail.objects.all()
    fromSet = set({})
    toSet = set({})
    for train in trains:
        fromSet.add(train.fromCity)
        toSet.add(train.toCity)    
    finalTrains = False    
    if request.method=='POST':
        fromCity = request.POST.get('fromCity')
        toCity = request.POST.get('toCity')
        trains = TrainDetail.objects.filter(Q(fromCity = fromCity) & Q(toCity = toCity))
        if trains:  
            finalTrains = True
        else:
            finalTrains = False 
        response = render(request,'app/railway.html',{'trains':trains,'finalTrains':finalTrains})
    else:
        response =  render (request,'app/railway.html',{'fromCity':fromSet,'toCity':toSet})   
    return HttpResponse(response)

@login_required
def railway_details_view(request,pk):
    totalitem=0
    product=TrainDetail.objects.get(pk=pk)
    if request.method=='POST':        
        user = request.user
        product_id = request.POST.get('prod_id')
        service = TrainDetail.objects.get(id=product_id)
        passengers = request.POST.get('passengers')
        BookedCart(user = user, services = service,passengers = passengers).save()
        return redirect('/train-booked')
    # item_already_in_cart=False
    # if request.user.is aunthenticated:
    #     totalitem=len(Cart.objects.filter(user=request.user))
    #     item_already_in_cart=cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/traindetails.html', {'product':product})

@login_required
def train_booked(request):
    if request.user.is_authenticated:
        user = request.user
        trains = BookedCart.objects.filter(user=user)
        amount = 0
        dbamount = 0
        n = 0
        for t in trains:
            dbamount = t.services.amount
            n = t.passengers
        for i in range(n):
            amount = amount + dbamount
        cart_product = [p for p in BookedCart.objects.all() if p.user==user]
        if cart_product:
            return render(request,'app/trainsbooked.html',{'trains':trains,'amount':amount})   
        else:
            return render(request,'app/emptytrain.html')    

@login_required
def delete_train(request,pk):
    c = BookedCart.objects.get(Q(id=pk) & Q(user=request.user))    
    c.delete()
    return redirect('/train-booked')    

# Movies
def movie_view(request,data=None):
    allMovies = Movie.objects.all()
    return render (request,'app/movies.html',{'allCycles':allMovies})     



def movie_details_view(request,pk):
    totalitem=0
    product=Movie.objects.get(pk=pk)
    # if request.method=='POST':        
    #     user = request.user
    #     product_id = request.POST.get('prod_id')
    #     return render(request,'app/moviebooking.html',{'product':product,'product_id':product_id})
    # item_already_in_cart=False
    # if request.user.is aunthenticated:
    #     totalitem=len(Cart.objects.filter(user=request.user))
    #     item_already_in_cart=cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/moviedetails.html', {'product':product})#, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

# Flight
def flight_view(request):
    trains = FlightDetail.objects.all()
    finalTrains = False
    fromSet = set({})
    toSet = set({})
    for train in trains:
        fromSet.add(train.fromCity)
        toSet.add(train.toCity)     
    if request.method=='POST':
        fromCity = request.POST.get('fromCity')
        toCity = request.POST.get('toCity')
        trains = FlightDetail.objects.filter(Q(fromCity = fromCity) & Q(toCity = toCity))
        if trains:  
            finalTrains = True
        else:
            finalTrains = False 
        response = render(request,'app/flights.html',{'trains':trains,'finalTrains':finalTrains})
    else:
        response =  render (request,'app/flights.html',{'fromCity':fromSet,'toCity':toSet})   
    return HttpResponse(response)

@login_required
def flight_details_view(request,pk):
    totalitem=0
    product=FlightDetail.objects.get(pk=pk)
    if request.method=='POST':        
        user = request.user
        product_id = request.POST.get('prod_id')
        service = FlightDetail.objects.get(id=product_id)
        passengers = request.POST.get('passengers')
        FlightCart(user = user, services = service,passengers = passengers).save()
        return redirect('/flight-booked')
    # item_already_in_cart=False
    # if request.user.is aunthenticated:
    #     totalitem=len(Cart.objects.filter(user=request.user))
    #     item_already_in_cart=cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/flightdetails.html', {'product':product})

@login_required
def flight_booked(request):
    if request.user.is_authenticated:
        user = request.user
        trains = FlightCart.objects.filter(user=user)
        amount = 0
        dbamount = 0
        n = 0
        for t in trains:
            dbamount = t.services.amount
            n = t.passengers
        for i in range(n):
            amount = amount + dbamount
        cart_product = [p for p in FlightCart.objects.all() if p.user==user]
        if cart_product:
            return render(request,'app/flightsbooked.html',{'trains':trains,'amount':amount})   
        else:
            return render(request,'app/emptyflight.html')    

@login_required
def delete_flight(request,pk):
    c = FlightCart.objects.get(Q(id=pk) & Q(user=request.user))    
    c.delete()
    return redirect('/flight-booked')    
       

# Bus       
def bus_view(request):
    trains = BusDetail.objects.all()
    finalTrains = False
    fromSet = set({})
    toSet = set({})
    for train in trains:
        fromSet.add(train.fromCity)
        toSet.add(train.toCity)     
    if request.method=='POST':
        fromCity = request.POST.get('fromCity')
        toCity = request.POST.get('toCity')
        trains = BusDetail.objects.filter(Q(fromCity = fromCity) & Q(toCity = toCity))
        if trains:  
            finalTrains = True
        else:
            finalTrains = False 
        response = render(request,'app/bus.html',{'trains':trains,'finalTrains':finalTrains})
    else:
        response =  render (request,'app/bus.html',{'fromCity':fromSet,'toCity':toSet})   
    return HttpResponse(response)

@login_required  
def bus_details_view(request,pk):
    totalitem=0
    product=BusDetail.objects.get(pk=pk)
    if request.method=='POST':        
        user = request.user
        product_id = request.POST.get('prod_id')
        service = BusDetail.objects.get(id=product_id)
        passengers = request.POST.get('passengers')
        BusCart(user = user, services = service,passengers = passengers).save()
        return redirect('/bus-booked')
    # item_already_in_cart=False
    # if request.user.is aunthenticated:
    #     totalitem=len(Cart.objects.filter(user=request.user))
    #     item_already_in_cart=cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/busdetails.html', {'product':product})  

@login_required
def bus_booked(request):
    if request.user.is_authenticated:
        user = request.user
        trains = BusCart.objects.filter(user=user)
        amount = 0
        dbamount = 0
        n = 0
        for t in trains:
            dbamount = t.services.amount
            n = t.passengers
        for i in range(n):
            amount = amount + dbamount
        cart_product = [p for p in BusCart.objects.all() if p.user==user]
        if cart_product:
            return render(request,'app/busbooked.html',{'trains':trains,'amount':amount})   
        else:
            return render(request,'app/emptybus.html')     

@login_required
def delete_bus(request,pk):
    c = BusCart.objects.get(Q(id=pk) & Q(user=request.user))    
    c.delete()
    return redirect('/bus-booked')  

# Search bar
def search_view(request):
    query = request.GET['search']
    result = Product.objects.filter(Q(brand__icontains=query) | Q(title__icontains=query)
        | Q(description__icontains=query) | Q(category__icontains=query) 
    )
    print(result)
    return render(request,'app/search.html',{'allCycles':result})               