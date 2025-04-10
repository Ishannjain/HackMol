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
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike")
]