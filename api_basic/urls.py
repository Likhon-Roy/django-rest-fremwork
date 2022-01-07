from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from rest_framework.generics import GenericAPIView
from .views import article_list, article_detail,ArticleApiView,ArticleDetails,GenericAPIView,ArticleViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article',ArticleViewset,basename='article')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls)),
    
    #path('article/', article_list),
    path('article/', ArticleApiView.as_view()),
    #path('detail/<str:pk>/',article_detail),
    path('detail/<str:pk>/',ArticleDetails.as_view()),
    path('generic/article/<int:id>/', GenericAPIView.as_view()),

]
