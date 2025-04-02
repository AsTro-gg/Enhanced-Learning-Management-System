from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView,GenericAPIView
from rest_framework.viewsets import ModelViewSet

class courseview(ModelViewSet):           # as these are just basic crud operations i use Modelview set, cause why not
    queryset = Course.objects.all()
    serializer_class = CourseSerialiser


class Userdetails(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialiser

    def get(self,request):
        userobjs = self.get_queryset()
        userserialiseddata = self.get_serializer(userobjs,many = True) # we use serialisation , convert data into json
        return Response(userserialiseddata.data,status=status.HTTP_200_OK)

    def post(self,request):
        userobjs = self.get_queryset()
        userserialiseddata = self.get_serializer(data = request.data) #we pass request which carries data we deserialise and convert json into complex data
        if request.method == "POST":
            if userserialiseddata.is_valid():
                user = userserialiseddata.save() #saving our user data in user
                user.set_password(user.password) #using set_passsword for hashing on user.password which is our given password.
                user.save()
                return Response(userserialiseddata.data,status=status.HTTP_201_CREATED)
            else:
                return Response(userserialiseddata.errors,status=status.HTTP_400_BAD_REQUEST)
        
class Userdetailsdynamic(GenericAPIView):
    def get(self,request,pk):
        try:    #lil error handling here and there
            queryset = User.objects.get(id=pk) #getting id value only
            serializer_class = UserSerialiser(queryset) #we dont need many = True as only one data respective to pk will come
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'errors':'User Not found'},status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        queryset = User.objects.get(id=pk) #getting id value only
        serializer_class = UserSerialiser(queryset,data=request.data)
        if serializer_class.is_valid():
            if "password" in request.data: # likely not necessary but wont hurt
                queryset.set_password(request.data['password'])  # we use usermodel's set_password function to hash password without duplication of request data
                queryset.save()

            serializer_class.save()
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request,pk):
        queryset = User.objects.get(id=pk) #getting id value only
        serializer_class = UserSerialiser(queryset,data = request.data,partial = True) #partial = true to update partial data
        if serializer_class.is_valid():
            if "password" in request.data: #necessary here
                queryset.set_password(request.data['password'])
                queryset.save()
            serializer_class.save()
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        queryset = User.objects.get(id=pk) #getting id value only
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
