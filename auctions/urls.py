from django.urls import path

from . import views

app_name = "auctions"


urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("new/", views.new, name="new"),
    path("listing/", views.no_listing, name="no_listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/watchlist/add", views.watchlist_add, name="watchlist_add"),
    path("listing/<int:id>/watchlist/remove", views.watchlist_remove, name="watchlist_remove"),
    path("listing/<int:id>/close", views.close, name="close"),
    path("listing/<int:id>/edit", views.edit, name="edit"),
    path("listing/<int:id>/bid", views.bid, name="bid"),
    
]
