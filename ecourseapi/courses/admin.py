from django.contrib import admin
from courses.models import Category, Course
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_date', 'updated_date']
    search_fields = ['name']
    list_filter = ['id', 'name', 'created_date']
    readonly_fields = ['my_image']
    form = CourseForm

    def my_image(self, course):
        if course.image: # nếu có ảnh thì trả về, còn không thì để null
            return mark_safe(f"<img width='390' src='/static/{course.image.name}'/>")

    class Media:
        css = {
            'all': {'/static/css/style.css'}
        }


# Register your models here.
admin.site.register(Category)
admin.site.register(Course, CourseAdmin)