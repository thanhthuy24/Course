from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = CloudinaryField(null=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id'] # tất cả truy vấn đều giảm theo id


class Course(BaseModel):
    name = models.CharField(max_length=255)
    description = RichTextField()
    image = models.ImageField(upload_to='courses/%Y/%m/')
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT)  # 'PROTECT' danh mục đụng tới khóa học thì không được xóa

    def __str__(self):
        return self.name