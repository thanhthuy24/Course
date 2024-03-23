from courses.models import Category, Course
from django.db.models import Count


def get_course(**kwargs):
    courses = Course.objects.filter(active=True)

    q = kwargs.get('q')
    if q:
        courses = courses.filter(name__icontain=q)

    cate_id = kwargs.get('category_id')
    if cate_id:
        courses = courses.filter(category_id=cate_id)

    return courses.order_by('-id')  # giảm theo id


# truy vấn thống kê
def count_courses_by_cate():
    return Category.objects.annotate(counter=Count('course__id')).values('id', 'name', 'counter').all()  # value chỉ định theo trường