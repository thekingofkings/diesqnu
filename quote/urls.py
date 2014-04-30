from django.conf.urls import patterns, url

from quote import views


urlpatterns = patterns( '',
    url(r'^$', views.index, name='index'),
    url(r'^aboutus$', views.about_us, name='aboutus'),
    url(r'^signup$', views.sign_up, name='signup')
)