from django.conf.urls import url
from . import views
from django.views.generic import View


app_name = 'shop'

urlpatterns = [
    url(r'^$', views.product_list, name = 'product_list'),
    url(r'^signup/$', views.UserFormView.as_view(), name = 'signup'),
    url(r'^login/$', views.user_login , name = 'user_login'),

    url(r'^login/$', views.user_logout, name = 'user_logout'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name = 'product_detail'),

]