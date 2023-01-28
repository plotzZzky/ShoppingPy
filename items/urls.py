from django.urls import path

from . import views


urlpatterns = [
    path('', views.show_app, name='show_lists'),
    path('item/new/', views.create_item, name='add_new_item'),
    #Listas
    path('all/id=<int:list_id>/', views.list_all, name='show_lists'),
    path('your/id=<int:list_id>/', views.get_your_list, name='get_list'),
    path('remove/id=<int:item_id>/', views.remove_item_from_list, name='remove_item_from_list'),
    path('add/<str:name>/', views.add_item_to_list, name='add_item_to_list'),
    path('your/<int:item_id>/amount=<int:amount>/', views.change_amount, name='change_amount'),
    path('clear/id=<int:list_id>/', views.clear_your_list, name='clear_your_list'),
]