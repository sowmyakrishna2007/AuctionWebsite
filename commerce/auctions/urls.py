from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close_bid/<int:id>", views.close_bid, name="close_bid"),
    path("watch/<int:id>", views.watch, name="watch"),
    path("comments/<int:id>", views.comments, name="comment"),
    path("categories", views.category_page, name="categories"),
    path("<str:category>", views.category, name="category")
]