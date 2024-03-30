from rest_framework.serializers import ModelSerializer
from courses.models import Category, Course, Lesson, Comment, Tag, User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(ModelSerializer):
    # phương thức trả ra kết quả đọc ra ngoài
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.image.url

        return req


class CourseSerializer(ItemSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'created_date']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(ItemSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'created_date']


# xem chi tiết bài học
class LessonDetailSerializer(LessonSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'tags']


class UserSerializer(ModelSerializer):
    # đè lại serializer để không lộ mật khẩu
    def create(self, validated_data):
        data = validated_data.copy() # sao chép dữ liệu
        u = User(**data) # lấy key làm tên tham số, lấy value được giá trị truyền vào
        u.set_password(u.password) # hàm băm của django
        # lưu User lại
        u.save()

        return u

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.avatar:
            rep['avatar'] = instance.avatar.url

        return rep

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']

        # không cho xem password
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class CommentSerializer(ModelSerializer):
    user = UserSerializer() # gọi để dưới class meta => xuất được hết thông tin của user
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'user']
