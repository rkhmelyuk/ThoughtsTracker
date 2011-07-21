from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('thought.views',
    # Examples:
    url(r'^$', 'index', name = 'index'),
    url(r'^post/$', 'post', name = 'post'),
    url(r'^edit/(?P<id>\w+)$', 'edit', name = 'edit'),
    url(r'^remove/(?P<id>\w+)$', 'remove', name = 'remove'),
    url(r'^thought/(?P<id>\w+)$', 'thought', name = 'thought'),
    url(r'^tag/(?P<tag>[^/]+)$', 'tag', name = 'tag'),
    url(r'^_internal/latestThoughtsPage/(?P<page>\d+)$', 'latestPage', name = 'latestPage'),
    url(r'^_internal/tagThoughtsPage/(?P<tag>[^/]+)/(?P<page>\d+)$', 'tagPage', name = 'tagPage'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
