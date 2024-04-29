from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from courses.models import Category, Course, Lesson, Comment, Like, Tag
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
import cloudinary
from django.urls import path


class MyAdminSite(admin.AdminSite):
    site_header = 'eCourse'

    def get_urls(self):
        return [path('cate-stats/', self.state_view)] + super().get_urls()

    def state_view(self, request):
        stats = Category.objects.annotate(counter=Count('course__id')).values('id', 'name', 'counter')
        return TemplateResponse(request, 'admin/stats.html',{
            'stats':stats
        })


admin_site = MyAdminSite(name='eCourse')


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class CateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_date', 'updated_date']
    search_fields = ['name']
    list_filter = ['id', 'name', 'created_date']
    readonly_fields = ['my_image']
    form = CourseForm

    def my_image(self, course):
        if course.image: # nếu có ảnh thì trả về, còn không thì để null
            if type(course.image) is cloudinary.CloudinaryResource:
                return mark_safe(f"<img width='390' src='{course.image.url}'/>")
            return mark_safe(f"<img width='390' src='/static/{course.image.name}'/>")

    class Media:
        css = {
            'all': {'/static/css/style.css'}
        }


# Register your models here.
admin_site.register(Category, CateAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson)
admin_site.register(Comment)
admin_site.register(Like)
admin_site.register(Tag)