from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = "investors"


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', views.index, name='index'),
    path('add-investor/', views.register, name='add-investor'),
    path('export_to_csv/', views.export_to_csv, name='export_to_csv'),
]