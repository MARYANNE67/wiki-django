from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry"),
    path('search/', views.search_page, name='search'),
    path('new/', views.new_page, name='new'),
    path('save/', views.save_page, name='save'),
    path('edit/', views.edit_page, name='edit'),
    path('random/', views.random_page, name='random')
]
