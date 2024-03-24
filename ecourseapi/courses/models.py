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
    image = CloudinaryField()
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT)  # 'PROTECT' danh mục đụng tới khóa học thì không được xóa

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=20, default='tag') # default = 'tag' - là nhãn trong thư viện react native sẽ render lên

    def __str__(self):
        return self.name


class Lesson(BaseModel):
    subject = models.CharField(max_length=255)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE) # cascade : khi xóa khóa học, tất cả bài học đều bị xóa theo
    content = RichTextField()
    image = CloudinaryField()
    tags = models.ManyToManyField(Tag)

    class Meta:
        # trong cùng khóa học, không có hai bài học trùng tên
        unique_together = ('subject', 'courses')


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255)


class Like(Interaction):
    class Meta:
        unique_together = ('lesson', 'user') # bấm like 1 lần, bấm 2 lần là unlike