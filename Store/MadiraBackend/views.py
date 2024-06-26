from django.shortcuts import render
from .serializers import ProductSerializer,UserSerializer,OrderSerializer,ShippingSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes,parser_classes,api_view,authentication_classes
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from .models import Products,Cart,Order,Customer,Shipping
import datetime

@api_view(['GET'])
def view_products(requests):
    products=Products.objects.all()
    serializer=ProductSerializer(products)
    return render(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def category_products(request,category):
    product=Products.objects.filter(category=category)
    serializer=ProductSerializer(product,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication,TokenAuthentication])
def cart(request,product_id):
    if request.method=="POST":
        customer=Customer.objects.get(user=request.user)
        product=get_object_or_404(Products,id=product_id)
        order,created=Order.objects.get_or_create(customer=customer,status=False)
        cart_item,created=Order.objects.get_or_create(order=order,product=product)
        if not created:
            cart_item.quantity+=1
            cart_item.save()
        return Response({'message':"Item added to cart"},status=status.HTTP_200_OK)

    return Response({"error":"Couldn't add to cart"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication,TokenAuthentication])
def cart_details(request):
    customer=request.user.customer
    order=Order.objects.filter(customer=customer,status=False).first()
    if order:
        serializer=OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response({"message":"cart is empty"},status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication,TokenAuthentication])
def update_cart(request,cart_id,action):
    cart_item=get_object_or_404(Cart,id=cart_id)
    if action=="add":
        cart_item.quantity+=1
    elif action=="sub":
        cart_item.quantity-=1
        if cart_item.quantity<=0:
            cart_item.delete()
    cart_item.save()
    return Response({'message':"cart updated"},status=status.HTTP_200_OK)

@api_view(['POST'])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication,TokenAuthentication])
def shipping(request):
    order=get_object_or_404(Order,customer=request.user.customer)
    if request.method=="POST":
        serializer=ShippingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user.customer,order=order)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='GET':
        shipping=get_object_or_404(customer=request.user.customer)
        serializer=ShippingSerializer(shipping)
        return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication,TokenAuthentication])
def process_order(request):
    transaction_id=datetime.datetime.now().timestamp()
    order,created=Order.objects.get_or_create(customer=request.user.customer,status=False)
    order.transaction_id=transaction_id
    total_price=request.data['total_price']
    if int(total_price)==order.get_total_amount:
        order.save()
        return Response({'message':"order verified"},status=status.HTTP_200_OK)
    
    else:
        return Response({'error':'total price is different'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@parser_classes([JSONParser,FormParser])
def register(request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user=User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        Token.objects.create(user=user)
        return Response({"messsage":"user registered"},status=status.HTTP_201_CREATED)


@parser_classes([JSONParser,FormParser])
@api_view(['POST'])
def login(request):
    user=get_object_or_404(User,username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"error":"Password didn't match"},status=status.HTTP_400_BAD_REQUEST)
    token,create=Token.objects.get_or_create(user=user)
    return Response({'token':token.key},status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.auth.delete()
    return Response({'message':"User logged out "})
