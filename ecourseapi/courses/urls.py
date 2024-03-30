<<<<<<< HEAD
from django.urls import path, include, re_path
from rest_framework import routers
from courses import views


r = routers.DefaultRouter()
=======
from django.urls import path, include
from courses import views
from rest_framework import routers


r = routers.DefaultRouter()

>>>>>>> origin
r.register('categories', views.CategoryViewSet, 'categories')
r.register('courses', views.CourseViewSet, 'courses')
r.register('lessons', views.LessonViewSet, 'lessons')
r.register('users', views.UserViewSet, 'users')

<<<<<<< HEAD
urlpatterns = [
    path('', include(r.urls))
]
=======

urlpatterns = [
    path('', include(r.urls))
]
>>>>>>> origin
