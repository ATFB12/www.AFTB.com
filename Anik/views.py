

from django.shortcuts import render,redirect
from .models import * 
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.http import JsonResponse
import json
import datetime


def store(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
          cartItems = order['get_cart_items']
     
     
     
     
     
     
     
     
     product=Product.objects.all()
     context = {'products':product,'cartItems':cartItems}
     return render(request,'Anik/store.html',context)
def checkout(request):
    if request.user.is_authenticated:
         customer = request.user.customer
         order, created = Order.objects.get_or_create(customer=customer, complete=False)
         items = order.orderitem_set.all()
         cartItems = order.get_cart_items
    else:
         items = []
         order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
         cartItems = order['get_cart_items']
         
    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'Anik/checkout.html', context)

def cart(request):
   if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
   else:
      cart=json.loads(request.COOKIES['cart'])
      print('Cart:',cart)
      items = []
      cartItems = order['get_cart_items']
      order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
      
   context = {'items':items, 'order':order,'cartItems':cartItems}
   return render(request, 'Anik/cart.html', context)


def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']
     print('Action:', action)
     print('Product:', productId)
     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)
     orderItem.save()
     if orderItem.quantity <= 0:
          orderItem.delete()
     return JsonResponse('Item was added', safe=False)
def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          total = float(data['form']['total'])
          order.transaction_id = transaction_id
          if total == order.get_cart_total:
               order.complete = True
          order.save()
          if order.shipping == True:
               ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
     else:
          print('User is not logged in')
     return JsonResponse('Payment submitted..', safe=False)

   




    
   
          