from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product,Cart,Order
from django.db.models import Q # to filter more than one condition
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.
# def about(request):
#     return HttpResponse("This is about page.")
# def home(request):
#     return HttpResponse("This is index page")
def edit(request,rid):
    print("Id to be edited: ",rid)
    print(type(rid))
    return HttpResponse("Id to be edit "+rid)
def addition(request,x1,x2):
    a=int(x1)+int(x2)
    print("Addition is :",a)
    return HttpResponse("Addition is : "+str(a))

class SimpleView(View):
    def get(self,request):
        return HttpResponse("Hello from django class based views")

def hello(request):
    context={}
    context['greet']='Good evening, we are learning DTL'
    context['x']=200
    context['y']=100
    context['l']=[10,20,30,40,50]
    context['products']=[
        {'id':1,'name':'samsung','cat':'mobile','price':2000},
        {'id':2,'name':'jeans','cat':'clothes','price':750},
        {'id':3,'name':'woodland','cat':'shoes','price':4500},
        {'id':4,'name':'Tshirt','cat':'clothes','price':450},
        ]
    return render(request,'hello.html',context)

    #------------------------ecomm project-------------------
def index(request):
    # userid=request.user.id
    # print("Id of logged in user: ",userid)
    # print(request.user.is_authenticated)
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    context['products']=p
    return render(request,'index.html',context)

def product_details(request,pid):
    p=Product.objects.filter(id=pid)
    context={}
    context['products']=p
    print(p)
    return render(request,'product_details.html',context)

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        # print(uname,"-" ,upass,"- ",ucpass)
        context={}
        if uname=="" or upass== "" or ucpass== "":
            context['errmsg']="Fields cannot be empty"
        elif upass!=ucpass:
            context['errmsg']="Password and confirm password didn't matched"
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User Created Successfully"
            except Exception:
                context['errmsg']="User with same name already Exist!!"
        return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def user_login(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        # print(uname)
        # print(upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields cann't be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass) #returns object
            print(u)  # print object parnika@gmail.com / return NONE if record is not in user table
            # print(u.id)
            # print(u.email)
            # print(u.username)
            # print(u.is_superuser)
            if u is not None:
                login(request,u) #start  session
                return redirect("/")
            else:
                context['errmsg']="Invalid Username and Password"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect("/")

def about(request):
    return render(request,'about.html')

def contactpage(request):
    return render(request,'contact.html')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        #ascending order
        col='price'
    else:
        #descending order
        col='-price'
    p=Product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    #data is not credintial so no we used GET method
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__lte=max)
    q2=Q(price__gte=min)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id # gives userid of which user is logged in
        # print(userid)
        # print(pid)
        u=User.objects.filter(id=userid)
        p=Product.objects.filter(id=pid)
        # print(u[0],p[0])
        #check product exits or not
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        context['products']=p
        if n==1:
            context['errmsg']="Product already exist!!!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product added successfully to cart!!"
            
        return render(request,'product_details.html',context)
    else:
        return redirect("/login")


def viewcart(request):
    #u=request.user.id   # id of logged in user 
    c=Cart.objects.filter(uid=request.user.id) # retrives details of logged in user
    context={}
    # print(c)  #[cart objet 3, cart object 4]
    # print(c[0].uid)
    # print(c[0].pid)
    # print(c[0].uid.username) 
    # print(c[0].uid.email)
    # print(c[0].pid.name)
    # print(c[0].pid.price)
    s=0
    np=len(c)
    for x in c:       #loop for calculate total price of all products of that logged in user
        s+=x.pid.price*x.qty
    print(s)
    context['total']=s
    context['data']=c
    context['n']=np
    return render(request,'cart.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect("/viewcart")

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)   #id=4 => queryset[object 4]
    print(c)  #give query set in list form
    #print(c[0])  #gived query object
    print(c[0].qty)
    if qv== '1':
        t=c[0].qty+1  #increment qty value
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect("/viewcart")

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    #print(oid)
    for x in c:
        #print(x.uid)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete() # from cart table after shifting into order table
    # return render(request,'placeorder.html')
    orders=Order.objects.filter(uid=userid)
    context={}
    context['data']=orders
    s=0
    np=len(orders)
    for x in orders:
        s=s+ x.pid.price*x.qty
    context['total']=s
    context['n']=np
    return render(request,'placeorder.html',context)

def removeorder(request,oid):
    p=Order.objects.filter(id=oid)
    #print(p)
    p.delete()
    return redirect('/placeorder')

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+ x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_pjmfONoAV5hhRJ", "2qLFlWxOv0vaA1jxWEEHwbcA"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    # print(payment)
    uemail=request.user.email
    print(uemail)
    context={}
    context['data']=payment
    context['uemail']=uemail
    context['uid']=request.user.id
    return render(request,'pay.html',context)
    # return HttpResponse("In makepayment section")

def sendusermail(request,uemail,uid):
    o=Order.objects.filter(uid=uid)
    msg=""
    print(o[0].pid.name)
    for x in o:
        # msg+=f"Your order is placed for {x.pid.name} and price for that product is {x.pid.price}"
        # print(msg)
        msg += f"""
        Thanks for visiting Estore...
        Product Name : {x.pid.name} and 
        Product Price : {x.pid.price}
        
        """
    send_mail(
        "Ekart order placed successfully!!",
        msg,
        "sharadagadadhe111@gmail.com",
        [uemail],
        fail_silently=False,
    )
    return HttpResponse("Mail sent successfully")