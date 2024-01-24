import requests
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions,viewsets
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from quickstart.models import Detail
from rest_framework import generics
from geopy.geocoders import GoogleV3


from quickstart.serializers import GroupSerializer,UserSerializer,DetailSerializer

# Create your views here.

class DetailsList(generics.ListCreateAPIView):
    serializer_class = DetailSerializer
    permission_classes = [permissions.IsAdminUser]  

    @csrf_exempt
    def get_queryset(self):
        queryset = Detail.objects.all()
        city = self.request.query_params.get('city')
        temperature = self.request.query_params.get('temperature')
        if city is not None:
            queryset = queryset.filter(city=city)
        if temperature is not None:
            queryset = queryset.filter(temperature=temperature)
        return queryset

class CombineDetails(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        print(data)
        if 'loc' in data:
            latitude, longitude = map(float, data['loc'].split(','))
        apiKey = 'a91c4d6539900a8a4ae3a222d4ef91f9'
        api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={apiKey}&units=metric'
        responsedata = requests.get(api_url)
        api_data = responsedata.json()
        fdata ={}
        fdata['name'] = api_data['name']
        fdata['main'] = api_data['main']
        return Response(fdata)


class UserViewSet(viewsets.ModelViewSet):
    queryset= User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_user_details(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

