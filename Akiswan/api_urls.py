from django.urls import include, path

urlpatterns = [
    path('base/', include('Base.api_urls')),
    path('user/', include('User.api_urls')),
    path('meat/', include('Meat.api_urls'))


]
