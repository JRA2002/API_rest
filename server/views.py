from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

@api_view(['POST'])
def login(request):
    
    print(request.data)
    
    user = get_object_or_404(User, username=request.data['username'])
    
    if not user.check_password (request.data['password']) : #compara el string con un dato que ya hemos pasado
        return Response({"error":"Invalid Password"},status=status.HTTP_400_BAD_REQUEST)
    
    token,bobi = Token.objects.get_or_create(user=user) #==> devuele una tupla,por eso agregue bobi
    serializer = UserSerializer(instance=user) #---instance es una keyword
    
    return Response({"token":token.key,"User":serializer.data},status=status.HTTP_200_OK)
    

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()
        
        token =  Token.objects.create(user=user)
        return Response({'token':token.key,'user':serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    
    print(request.user)
    
    return Response("you are looged with {}".format(request.user.username),status=status.HTTP_200_OK)
