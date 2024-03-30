from rest_framework import viewsets, generics, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
<<<<<<< HEAD
from courses.models import Category, Course, Lesson, Like, Comment, Tag, User
from courses import serializers, paginators


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):

 # nếu chỉ viewset thì chỉ tạo ra list, retrieve, create chứ chưa tạo ra API nào
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True) # lấy những object có active = True
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.ItemPaginator

    # lọc theo kw
    def get_queryset(self):
        # lấy queryset gốc ra trước
        queryset = self.queryset

        if self.action.__eq__('list'):
            # ../?q= => thêm query
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            cate_id = self.request.query_params.get('category_id')
            if cate_id:
                # cate_id khóa ngoại nên chú ý lúc viết
                queryset = queryset.filter(category_id=cate_id) #khi để category__id => tiến hành join bảng

        return queryset

    # Url: /courses/{course_id}/lessons/?q=
    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(self, request, pk): # tham số pk chỉ có khi detail=True
        # tập hợp những bài học của khóa học đó
        lessons = self.get_object().lesson_set.filter(active=True)

        q = request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)

        # trả về cái dữ liệu mà nó serializer cho mình
=======
from courses.models import Category, Course, Lesson, User
from courses import serializers, paginators


class CategoryViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    # Permission_class = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.ItemPaginator

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)

        cate_id = self.request.query_params.get('cate_id')
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)

        return queryset

    @action(methods=['get'], url_path='lesson', detail=True) # detail=true thì mới có biến pk
    def get_lesson(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
>>>>>>> origin
        return Response(serializers.LessonSerializer(lessons, many=True).data,
                        status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ModelViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
<<<<<<< HEAD
    serializer_class = serializers.LessonDetailSerializer

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        # truy vấn bài cmt
        comments = self.get_object().comment_set.select_related('user').all()
        # cmt cần người tạo, nếu không có select_related =>
        # nếu có 100 cmt => mất 100 lần join để lấy từng user ra.

        return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)
=======
    serializer_class = serializers.LessonDetailsSerializer
>>>>>>> origin


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
<<<<<<< HEAD

    # vì mặc định không nhận file => dùng parsers
    parser_classes = [parsers.MultiPartParser,]
=======
    parser_classes = [parsers.MultiPartParser, ]
>>>>>>> origin
