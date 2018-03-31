
from django.conf.urls import url, include
from notesmerge import views
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

admin.autodiscover()

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'merges_api', views.MergeViewSet, base_name="merges")
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
  url(r'^$', TemplateView.as_view(template_name='notesmerge/build/index.html'), name='index'),
  url(r'^merges$', TemplateView.as_view(template_name='notesmerge/build/index.html'), name='index'),
  url(r'^merge/(\d+)$', TemplateView.as_view(template_name='notesmerge/build/index.html'), name='index'),
  url(r'^logout$', TemplateView.as_view(template_name='notesmerge/build/index.html'), name='index'),
  url(r'^login$', TemplateView.as_view(template_name='notesmerge/build/index.html'), name='index'),
  url(r'^logout$', TemplateView.as_view(template_name='notesmerge/build/index.html'), name='index'),
  url(r'^', include(router.urls)),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  url(r'^do_merge/$', views.DoMerge.as_view(), name='do_merge'),
  url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
  url(r'^admin/', include(admin.site.urls)),
 # url(r'^accounts/login/$', auth_views.login),
  #url('^accounts/', include('django.contrib.auth.urls')),

  #url('^accounts/', include('django.contrib.auth.urls')),

]
