from django.urls import path
from django.conf.urls import url


from ReCAST import views

urlpatterns = [
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('sendMail/', views.sendMail),
    #path('register_suc/', views.register_suc), #successfully register


    path('createTask/', views.createTask),
    url(r'^upload/$',views.upload),
    path('config/', views.config),
    path('advOpt/', views.advOpt),
    path('run/', views.run),
    path('adv/', views.adv),
    path('modify/', views.modify),
    path('details/', views.details),
    path('export/', views.export),
    path('delete/', views.delete),

    path('viewHistory/', views.viewHistory),
    path('search/', views.search),

    path('save/', views.save),
    path('discard/', views.discard),
    path('quit/', views.quit),

    path('downloadManual/', views.downloadManual),
    path('checkUsername/', views.checkUsername),
    path('update/', views.update),
    path('restore/', views.restore),

    path('render/', views.display),


    #path('reset/code', views.getActiveCode),

    path('reset/', views.reset),
    path('doreset/', views.doreset),
    path('regist/', views.regist),
    url(r'^', views.default),
]
