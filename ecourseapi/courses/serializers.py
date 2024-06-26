from courses.models import Category, Course, Lesson, Comment, Tag, User
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    # phương thức trả ra kết quả đọc ra ngoài
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.image.url

        return req


class CourseSerializer(ItemSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'created_date']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(ItemSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'created_date']

# xem chi tiết bài học
class LessonDetailsSerializer(LessonSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'tags']


class AuthenticatedLessonDetailsSerializer(LessonDetailsSerializer):
    #
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson): # lesson là instance của model
        request = self.context.get('request')
        if request:
            # muốn biết user đã like bài này chưa,
            # lấy danh sách các like (truy vấn ngược - like_set)
            # trường exists - kiểm tra tồn tại
            return lesson.like_set.filter(user=request.user, active=True).exists()

    class Meta:
        model = LessonDetailsSerializer.Meta.model
        fields = LessonDetailsSerializer.Meta.fields + ['liked']


class UserSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']

        # không cho xem password
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer() # gọi để dưới class meta => xuất được hết thông tin của user
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'user']

