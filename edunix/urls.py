from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('', include('home.urls')),
]


admin.site.site_header = "Edunix Admin"
admin.site.site_title = "Edunix Admin Portal"
admin.site.index_title = "Welcome to Edunix Admin Portal"
