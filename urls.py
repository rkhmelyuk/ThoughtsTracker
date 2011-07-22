from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('thought.views.app',
    url(r'^$', 'index', name = 'index'),
    url(r'^post/$', 'post', name = 'post'),
    url(r'^edit/(?P<id>\w+)$', 'edit', name = 'edit'),
    url(r'^remove/(?P<id>\w+)$', 'remove', name = 'remove'),
    url(r'^thought/(?P<id>\w+)$', 'thought', name = 'thought'),
    url(r'^tag/(?P<tag>[^/]+)$', 'tag', name = 'tag'),
    url(r'^_internal/latestThoughtsPage/(?P<page>\d+)$', 'latestPage', name = 'latestPage'),
    url(r'^_internal/tagThoughtsPage/(?P<tag>[^/]+)/(?P<page>\d+)$', 'tagPage', name = 'tagPage'),

    url(r'^settings/$', 'appSettings', name = 'settings'),
)

urlpatterns += patterns('thought.views.api',
    url(r'^api/searchTags/(?P<keyword>[^/]+)$', 'searchTags', name = 'searchTags'),
)