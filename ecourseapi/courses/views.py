from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from courses.models import Category, Course, Lesson, Like, Comment, Tag, User
from courses import serializers, paginators, perms


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
from courses.models import Category, Course, Lesson, User
from courses import serializers, paginators


class CategoryViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    # Permission_class = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
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
        return Response(serializers.LessonSerializer(lessons, many=True).data,
                        status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ModelViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailsSerializer

    def get_serializer_class(self):
        if self.request.user.is_authenticated: # lấy user coi chứng thực chưa
            return serializers.AuthenticatedLessonDetailsSerializer

        return self.serializer_class

    # phải xác thực mới thêm comment được
    def get_permissions(self):
        if self.action in ['add_comment', 'like']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        # truy vấn bài cmt
        comments = self.get_object().comment_set.select_related('user').all()
        # cmt cần người tạo, nếu không có select_related =>
        # nếu có 100 cmt => mất 100 lần join để lấy từng user ra.

        paginator = paginators.CommentPaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)
    #serializer_class = serializers.LessonDetailsSerializer

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        # tập hợp các comment của lesson
        c = self.get_object().comment_set.create(user=request.user, content=request.data.get('content')) # trả về đối tượng lesson đại diện cho khóa chính pk mà mình gửi lên
        # c = Comment.objects.create(user=, lesson=, content=)

        return Response(serializers.CommentSerializer(c).data,
                        status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        # get_or_create : kiểm tra có tồn tại user mà lesson này trong db chưa,
        # nếu chưa có => create đối tượng like mới => create = true
        # nếu có rồi, create = false
        li, created = Like.objects.get_or_create(lesson=self.get_object(),user=request.user)

        if not created:
            li.active = not li.active
            li.save()

        return Response(serializers.AuthenticatedLessonDetailsSerializer(self.get_object()).data)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer

    # vì mặc định không nhận file => dùng parsers
    parser_classes = [parsers.MultiPartParser,]

    def get_permissions(self):
        if self.action in ['current_user']: # nếu nằm trong danh sách current user này
            return [permissions.IsAuthenticated()] # có dấu ngoặc để tạo đối tuượng
        return [permissions.AllowAny()]

    # tạo api rời
    @action(methods=['get', 'patch'],url_path='current_user', detail=False) # vì nếu cho truyền lên không an toàn, user này biết
    def current_user(self, request):                                # biết được ID của user khác sẽ fetch lấy dữ liệu được
        user = request.user
        if request.method.__eq__('PATCH'):
            # request.data => cục từ điển được gửi lên nằm trong biến data (nếu nằm trong body)
            for k, v in request.data.items(): # k -key; v - value on postman
                setattr(user, k, v) # => user.k = v
            user.save()

        return Response(serializers.UserSerializer(request.user).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    # tạo chứng thực riêng
    permission_classes = [perms.CommentOwner]

