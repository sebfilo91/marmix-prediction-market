import django
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.core.urlresolvers import reverse
from rest_framework.urlpatterns import format_suffix_patterns
import Market

admin.autodiscover()

urlpatterns = patterns('Market',
    ##-------------------------------------------------
    ##
    ##  URLs des vues
    ##
    ##-------------------------------------------------
    url(r'^$','views.home'),
    url(r'^home/$','views.home',name='home'),
    url(r'^claims/$','views.claims',name='list_claim'),
    url(r'^portfolio/$','views.portfolio',name='portfolio'),
    url(r'^dashboard_user/$','views.dashboard_user',name='dashboard_user'),
    url(r'^leaderboard/$','views.leaderboard',name='leaderboard'),
    url(r'^claim_create/$','views.claim_create',name='claim_create'),
    url(r'^historic/$','views.historic',name='historic'),
    url(r'^claim_info/(?P<id>\d+)/$','views.claim_info',name='claim_info'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^order_create/(?P<claim_id>\d+)/$', 'views.order_create', name='order_create'),
    url(r'^signup/$', 'views.signup',name="signup"),
    ##-------------------------------------------------
    ##
    ##  URL des Web Services
    ##
    ##-------------------------------------------------
    url(r'^claim/$', Market.views.ClaimList.as_view()),
    url(r'^claim/(?P<id>\d+)/$', Market.views.ClaimDetail.as_view()),
    url(r'^order/$', Market.views.OrderList.as_view()),
    url(r'^order/(?P<id>\d+)/$', Market.views.OrderDetail.as_view()),

)

urlpatterns += patterns('',
    ##-------------------------------------------------
    ##
    ##  Vues génériques de Django
    ##
    ##-------------------------------------------------
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'market/login.html'},name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse('home')},name='logout'),
    url(r'^password_reset/$','django.contrib.auth.views.password_reset_confirm',{'template_name': 'market/password_reset.html','post_reset_redirect':reverse('home')},name='password_reset'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

)

urlpatterns = format_suffix_patterns(urlpatterns)
