from django.urls import path
#from ecomm_app import views
from . import views
from .views import SimpleView
#from ecomm_app.views import SimpleView
urlpatterns = [
    path('about',views.about),
    path('',views.home),
    path('edit/<rid>',views.edit),
    path('addition/<x1>/<x2>',views.addition),
    path('myview',SimpleView.as_view()),
    path('hello',views.hello)
]