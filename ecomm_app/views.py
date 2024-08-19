from django.shortcuts import render,HttpResponse
from django.views import View
# Create your views here.
def about(request):
    return HttpResponse("This is about page.")
def home(request):
    return HttpResponse("This is index page")
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