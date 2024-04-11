from rest_framework import permissions


class CommentOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        # kiểm tra quyền đăng nhập rồi and thêm điều kiện: người đăng nhập == người comment
        return super().has_permission(request, view) and request.user == comment.user



