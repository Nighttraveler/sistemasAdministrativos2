from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from django.views import generic
from django.core.urlresolvers import reverse_lazy



app_name ='authentication'

urlpatterns = [
    url(r'^$',
            generic.TemplateView.as_view(
                template_name = 'authentication/index.html'),
                name='index'),

    url(r'^dashboard/$',
            generic.TemplateView.as_view(
                template_name = 'authentication/dashboard.html'),
                name='dashboard'),

    url (r'^accounts/logout/$', auth_views.logout,
        {'next_page':reverse_lazy('authentication:index')},
        name='logout' ),

]
