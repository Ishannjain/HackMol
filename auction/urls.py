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
    path("watchlist/<int:user_id>",views.watchlist,name="watchlist"),
    path("posts/",views.posts, name="posts"),
    path("newPost/", views.newPost, name="newPost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
]