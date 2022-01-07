from http.client import responses
from os import stat
from django.http import HttpResponse
from rest_framework import serializers
import rest_framework
from rest_framework.serializers import ModelSerializer, Serializer
from .models import Article
from api_basic.serializers import ArticleSerializer
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import generics
from rest_framework import mixins

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# Model Viewsets
class ArticleViewset(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()



# Generic viewsets
"""class ArticleViewset(viewsets.GenericViewSet,mixins.ListModelMixin, mixins.CreateModelMixin, 
                    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()"""



# Viewsets

"""class ArticleViewset(viewsets.ViewSet):

    def list(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many = True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status= status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(slef, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return HttpResponse(status= status.HTTP_404_NOT_FOUND)
        #article = get_object_or_404(queset,pk=pk)
        

        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk = None):
        article = Article.objects.get(pk=pk)
        serializer= ArticleSerializer(instance=article,data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)"""


# Generic api view

class GenericAPIView(generics.GenericAPIView , mixins.ListModelMixin,mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'
    #authentication_classes=[SessionAuthentication, BasicAuthentication ]
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request,id)
        else:
            return self.list(request)

    def post(self,request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request,id)

    def delete(self,request,id):
        return self.destroy(request,id)


# class based api

class ArticleApiView(APIView):
    def get(self,request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status = status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class ArticleDetails(APIView):
    def get_object(self,pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404
            #return HttpResponse(status = status.HTTP_404_NOT_FOUND)

    def get(self,request, pk):
        article = self.get_object(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self,request,pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(instance=article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# decorator, function based api

@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['PUT','GET','DELETE'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return HttpResponse(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



