from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('petsDetail/<int:pid>',views.petsDetail, name='petsDetail'),
    path('view/', views.viewcart, name='view'),
    path('addCart/<int:pid>',views.addCart,name="addCart"),
    path('remove/<int:pid>',views.remove,name='remove'),
    path('search/',views.search,name='search'),
    path('range/',views.range,name="range"),
    path('catList/',views.catlist,name="catList"),
    path('dogList/',views.doglist,name="dogList"),
    path('sort/',views.sort,name="sort"),
    path('sortd/',views.sortd,name="sortd"),
    path('updateqty/<int:uval>/<int:pid>/',views.updateqty,name="updateqty"),
    path('register',views.register_user,name="register"),
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('viewOrder/',views.vieworder,name="viewOrder"),
    path('payment/',views.makepayment,name="payment"),
    path('insertpets/',views.insertpets,name="insertpets"),
] 