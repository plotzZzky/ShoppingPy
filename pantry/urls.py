from django.urls import path

from . import views


urlpatterns = [
    # Pantry
    path('', views.view_pantry, name='view_pantry'),
    path('list=<int:list_id>/', views.get_pantry_list, name='get_list_pantry'),
    # Mange Pantry
    path('add/id=<int:list_id>/', views.add_to_pantry, name='add_to_pantry'),
    path('remove=<int:item_id>/', views.remove_from_pantry, name='remove_from_pantry'),
    path('clear/id=<int:list_id>/', views.pantry_clear, name='pantry_clear'),
    # Properties
    path('item=<int:item_id>/', views.get_properties, name='get_properties'),
    path('item=<int:item_id>/date=<path:date>/', views.set_properties, name='set_properties'),
]