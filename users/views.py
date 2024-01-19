from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import UserAccount, Trust
from users.serializers import Users_Serializer, Trust_Serializer

@api_view(['POST'])
def User_Add(request):
    serializer = Users_Serializer(data = request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['GET'])
def User_View(request, pk):
    carts = UserAccount.objects.filter(username = pk)
    serializer = Users_Serializer(carts, many=True)

    return Response(serializer.data)

@api_view(['PUT'])
def User_Update(request, pk):
    cart = UserAccount.objects.get(username = pk)
    serializer = Users_Serializer(instance=cart, data = request.data)
    
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['GET'])
def Trust_View(request, pk):
    st = []
    try:
        Tr = Trust.objects.get(User_ID = pk)
          
        if Tr.User_ID:
            st = [{'Trusted':'Yes'}]

        else:
            st = [{'Trusted':'No'}]

    except:
        st = [{'status':'No'}]

    return Response(st)