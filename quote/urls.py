from django.conf.urls import patterns, url

from quote import views


urlpatterns = patterns( '',
    url(r'^$', views.index, name='index'),
    url(r'^aboutus$', views.about_us, name='aboutus'),
    url(r'^signup$', views.sign_up, name='signup'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^search$', views.search, name='search'),
    url(r'^createuser$', "quote.views.createUser")
)