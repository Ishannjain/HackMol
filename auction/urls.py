from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/",views.create_listing,name="create"),
    path("category/<str:category_name>",views.category,name="category"),
    path("listing/<int:listing_id>",views.listing,name="listing"),
    path("watchlist/<int:user_id>",views.watchlist,name="watchlist")
]