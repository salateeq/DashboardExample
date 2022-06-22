from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sources', views.sources, name='sources'),
    path('internet_users/<str:countryname>/<str:date2>', views.internet_users, name='internet_users'),
    path('internet_access/<str:countryname>/<str:date2>', views.internet_access, name='internet_access'),
    path('internet_access_in_schools/<str:countryname>/<str:date2>', views.internet_access_in_schools, name='internet_access_in_schools'),
    path('individuals_using_the_internet/<str:countryname>/<str:date2>', views.individuals_using_the_internet, name='individuals_using_the_internet'),
]