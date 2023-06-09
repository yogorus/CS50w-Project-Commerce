from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name='create'),
    path('categories', views.categories, name='categories'),
    path('listing/<int:id>', views.listing, name='listing'),
    path('listing/<int:id>/addwatchlist', views.addwatchlist, name='addwatchlist'),
    path('listing/<int:id>/close', views.close, name='close'),
    path('watchlist', views.watchlist, name='watchlist')
]
