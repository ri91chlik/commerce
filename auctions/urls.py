from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("show_category", views.show_category, name="show_category"),
    path("create", views.create_listing, name="create"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("show_watchlist/<int:id>/", views.show_watchlist, name="show_watchlist"),
    path("addWatchList/<int:id>/", views.addWatchList, name="addWatchList"),
    path("removeWatchList/<int:id>/", views.removeWatchList, name="removeWatchList"),
    path("comment1/<int:id>/", views.comment1, name="comment1"),
    path("AnnexBid/<int:id>/", views.AnnexBid, name="AnnexBid"),
    path("listing/<int:id>/", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("terminateAuction/<int:id>/", views.terminateAuction, name="terminateAuction"),
]
