
from django.urls import path
from django.conf.urls import url


from ReCAST import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    #path('register_suc/', views.register_suc), #successfully register
    path('reset/', views.reset),
    path('reset/code', views.getActiveCode),

    path('createTask/', views.createTask),
    url(r'^upload/$',views.upload),
    path('config/', views.config),
    path('advOpt/', views.advOpt),
    path('run/', views.run),
    path('adv/', views.adv),
    path('modify/', views.modify),
    path('export/', views.export),

    path('viewHistory/', views.viewHistory),
    path('search/', views.search),

    path('save/', views.save),
    path('discard/', views.discard),
    path('quit/', views.quit),

    path('downloadManual/', views.downloadManual),

    path('render/', views.display),
    # Default page

    url(r'^', views.default),
]
