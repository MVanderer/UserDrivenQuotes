from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^dashboard$',views.dashboard),
    url(r'^sign_up$',views.sign_up),
    url(r'^log_in$',views.log_in),
    url(r'^log_off$',views.log_off),
    url(r'^user/(?P<id>\d+)$',views.user_quotes),
    url(r'^myaccount/(?P<id>\d+)$',views.myaccount),
    url(r'^quote_submit$',views.quote_submit),
    url(r'^quote_delete/(?P<id>\d+)$',views.quote_delete),
    url(r'^account_update$',views.account_update),
    url(r'^like/(?P<id>\d+)$',views.like),
]