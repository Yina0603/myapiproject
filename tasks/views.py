# tasks/views.py
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer, UserRegisterSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        # 自動將新任務的 owner 設為目前認證的使用者
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(owner=user)
        # 支援使用 query param 過濾完成狀態，如 ?completed=true
        completed_param = self.request.query_params.get('completed')
        if completed_param is not None:
            completed = completed_param.lower() in ['true', '1']
            queryset = queryset.filter(is_completed=completed)
        return queryset


@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # 建立新用戶
        return Response({"message": "註冊成功，請使用您的帳號密碼登入。"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)