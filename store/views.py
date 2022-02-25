from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookiecart, cartdata, guestorder

# Create your views here.

def store(request):
    data = cartdata(request)
    cartitems = data['cartitems']

    products = Product.objects.all()
    context = {'products':products, 'cartitems':cartitems, 'shipping':False}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartitems':cartitems, 'shipping':False}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']


    context = {'items':items, 'order':order, 'cartitems':cartitems, 'shipping':False}

    return render(request, 'store/checkout.html', context)

def updateitem(request):
    data =  json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action :', action)
    print('ProductId :', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()


    return JsonResponse('Item was added', safe=False)

def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    print(transaction_id)
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)

    else:
        customer, order = guestorder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
                customer = customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                street=data['shipping']['street'],
                building=data['shipping']['building'],
                )


    return JsonResponse('Payment complete !', safe=False)
