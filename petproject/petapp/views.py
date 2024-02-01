from django.shortcuts import render,HttpResponse,redirect
from .models import Pet,CartPet,Order
from django.db.models import Q
from .forms import CreateUserForm,AddPet
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
import random,razorpay
# Create your views here.
def index(request):
    pets = Pet.objects.all()
    context={}
    context['pets']= pets
    return render(request,"index.html",context)

def petsDetail(request,pid):
    pets = Pet.objects.get(sid = pid)
    return render(request,"view.html",{'pets':pets})

def viewcart(request):
    if request.user.is_authenticated:
        allpets = CartPet.objects.filter(user = request.user)
    else:
        return redirect("/login")
    context = {}
    context['cart_items']=allpets
    total_price = 0
    for x in allpets:
        total_price += (x.pet.price * x.quantity)
        print(total_price)
        context['total'] = total_price
        length = len(allpets)
        context['items'] = length
    return render(request,"cart.html",context)

def addCart(request,pid):
    pets = Pet.objects.get(sid = pid)
    user = request.user if request.user.is_authenticated else None
    print(pets)
    if user :
        cart_item,created = CartPet.objects.get_or_create(pet=pets,user = user)
        print(cart_item,created)
    else:
        cart_item,created = CartPet.objects.get_or_create(pet=pets,user = None)
    if not created:
        cart_item.quantity +=1
    else:
        cart_item.quantity =1
    cart_item.save()
    return redirect("/view")

def remove(request,pid):
    p = CartPet.objects.filter(sid = pid)
    p.delete()
    return redirect("/viewcart")

def search(request):
    query = request.POST['q']
    print(f"Received Item is {query}")
    if not query:
        result = Pet.objects.all()
    else:
        result = Pet.objects.filter(
            Q(name__icontains = query)|
            Q(type__icontains = query)|
            Q(price__icontains = query)
        )
    return render(request,'search.html',{'results':result,'query':query})

def range(req):
    if req.method == "GET":
        return redirect("/")
    else:
        p1 = req.POST.get("min")
        p2 = req.POST.get("max")
        print(p1,p2)
    if p1 is not None and p2 is not None and p1 !="" and p2 !="":
        queryset = Pet.petss.get_price_range(p1,p2)
        context={'pets':queryset}
    return render(req,"index.html",context)
    
def doglist(req):
    queryset = Pet.petss.dog_list()
    context={'pets':queryset}
    return render(req,'index.html',context)

def catlist(req):
    queryset = Pet.petss.cat_list()
    context={'pets':queryset}
    return render(req,'index.html',context)

def sort(request):
    queryset = Pet.objects.all().order_by("price")
    context = {'pets':queryset}
    return render(request,'index.html',context)

def sortd(request):
    queryset = Pet.objects.all().order_by("-price")
    context = {'pets':queryset}
    return render(request,'index.html',context)

def updateqty(req,uval,pid):
    pets = Pet.objects.get(sid = pid)
    user = req.user
    c =CartPet.objects.filter(pet = pets,user = user)
    print(c)
    print(c[0])
    print(c[0].quantity)
    if uval == 1:
        a = c[0].quantity + 1
        c.update(quantity = a)
        print(c[0].quantity)
    elif uval==0:
        a = c[0].quantity - 1
        c.update(quantity = a)
        print(c[0].quantity)
    return redirect("/cart")

def register_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,("User Created Successfully"))
            return redirect("/login")
        else:
            messages.error(request,("Username or Password Invalid !!"))
    context = {'form':form}
    return render(request,"register.html",context)

def login_user(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("Logged in Successfully"))
            return redirect("/")
        else:
            messages.error(request,"Error! Try Again!!")
            return redirect('/login')
        
    return render(request,"login.html")

def logout_user(request):
    logout(request)
    messages.success(request,("You are Logout"))
    return redirect("/")

def vieworder(req):
    c = CartPet.objects.filter(user = req.user)
    context={}
    context = {}
    context['cart_items']=c
    total_price = 0
    for x in c:
        total_price += (x.pet.price * x.quantity)
        print(total_price)
        context['total'] = total_price
        length = len(c)
        context['items'] = length
    return render(req,"vieworder.html",context)

def makepayment(req):
    c = CartPet.objects.filter(user = req.user)
    oid = random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id = oid, pet = x.pet, user = req.user, quantity = x.quantity)
    orders = Order.objects.filter(user = req.user,is_completed = False)
    total_price = 0
    for x in orders:
        total_price += (x.pet.price * x.quantity)
        oid = x.order_id
        print(oid)
    client = razorpay.Client(auth=("rzp_test_59qXQ6StJGhFat", "GvxJTHsElnI5WdRxpcWFzd02"))

    data = {
        "amount": total_price * 100,
        "currency": "INR",
        "receipt": "oid"
        }
    payment = client.order.create(data = data)
    context = {}
    context['data'] = payment
    context['amount'] = payment["amount"]
    c.delete()
    orders.update(is_completed = True)
    return render(req,"payment.html",payment)

def insertpets(req):
    if req.user.is_authenticated:
        user = req.user
        if req.method == "GET":
            form = AddPet()
            return render(req,"insertpets.html",{'form':form})
        else:
            form = AddPet(req.POST,req.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(req,("Pet Inserted Successfully"))
                return redirect("/")
            else:
                messages.error(req,"incorrect data")
                return render(req,"insertpets.html",{'form':form})
                
    else:
        return redirect('/login')