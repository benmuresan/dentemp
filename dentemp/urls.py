from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^new_user/', "dentemp_site.views.new_user", name='new_user'),
                       url(r'^log_in/', "dentemp_site.views.log_in", name='log_in'),
                       url(r'^log_out/', "dentemp_site.views.log_out", name='log_out'),
                       url(r'^elements/', "dentemp_site.views.elements", name='elements'),
                       url(r'^generic/', "dentemp_site.views.generic", name='generic'),
                       url(r'^profile/', "dentemp_site.views.profile", name='profile'),
                       url(r'^user_dash/', "dentemp_site.views.user_dash", name='user_dash'),
                       url(r'^office_dash/', "dentemp_site.views.office_dash", name='office_dash'),
                       # url(r'^register/', "dentemp_site.views.register", name='register'),
                       url(r'^new_office/', "dentemp_site.views.new_office", name='new_office'),
                       url(r'^create_user/', "dentemp_site.views.create_user", name='create_user'),
                       url(r'^create_office/', "dentemp_site.views.create_office", name='create_office'),
                       url(r'^account_disabled/', "dentemp_site.views.account_disabled", name='account_disabled'),
                       url(r'^incorrect_login/', "dentemp_site.views.incorrect_login", name='incorrect_login'),
                       url(r'^', "dentemp_site.views.index", name='index'),
)
