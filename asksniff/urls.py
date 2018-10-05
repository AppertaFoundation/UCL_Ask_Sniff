"""asksniff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from iPoorly import views


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^admin/django/', admin.site.urls),
    url(r'^admin/(?P<symptom_name>[\w]+)$', views.admin_symptom, name='admin_symptom'),
    url(r'^admin/heading/(?P<heading_id>[\d]+)$', views.admin_headings, name='admin_headings'),
    url(r'^admin/subheading/(?P<heading_id>[\d]+)/(?P<sub_heading_id>[\d]+)$', views.admin_subheadings, name='admin_subheadings'),
    url(r'^$', views.index, name='index'),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^homepage/$', views.homepage, name='homepage'),
    url(r'^accounts/login/', views.user_login, name='user_login'),
    url(r'^accounts/signup/', views.user_signup, name='user_signup'),
    url(r'^accounts/logout/', views.user_logout, name='user_logout'),
    url(r'^accounts/forgot/', views.forgot_password, name='forgot_password'),
    url(r'^child/$', views.my_child, name='myChild'),
    url(r'^child/manage/', views.child_manage, name='child_manage'),
    url(r'^childDelete/', views.child_delete, name='child_delete'),
    url(r'^childActivate/', views.child_activate, name='child_activate'),
    url(r'^disclaimer/', views.disclaimer, name='disclaimer'),
    url(r'^noUser/age/$', views.age, name='age'),
    url(r'^symptom/(?P<symptom_name>[\w]+)$', views.symptom, name='symptom'),
    url(r'^symptom/delete/$', views.symptom_delete, name='symptom_delete'),
    url(r'^symptom/information/(?P<heading_id>[\d]+)$', views.symptom_heading, name='symptom_heading'),
    url(r'^map/$', views.location_map, name='map'),
    url(r'^search/$', views.search, name='search'),
    url(r'^diary/$', views.diary, name='diary'),
    url(r'^diary/(?P<child_id>[\d]+)$', views.diary_logs, name='diary_logs'),
    url(r'^diary/delete/$', views.diary_delete, name='diary_delete'),
    url(r'^all_urls/$', views.all_urls, name='all_urls'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
