from django.urls import path, include, re_path
from rest_framework import routers
from courses import views


r = routers.DefaultRouter()

from django.urls import path, include
from courses import views
from rest_framework import routers


r = routers.DefaultRouter()

r.register('categories', views.CategoryViewSet, 'categories')
r.register('courses', views.CourseViewSet, 'courses')
r.register('lessons', views.LessonViewSet, 'lessons')
r.register('users', views.UserViewSet, 'users')
r.register('comments', views.CommentViewSet, 'comments')

urlpatterns = [
    path('', include(r.urls))
]

urlpatterns = [
    path('', include(r.urls))
]
