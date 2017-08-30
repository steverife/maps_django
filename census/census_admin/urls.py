from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'census_admin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include('census_api.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
