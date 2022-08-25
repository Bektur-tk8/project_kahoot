from rest_framework.viewsets import ModelViewSet

from .serializers import GroupSerializer
from .models import UserGroup


class GroupViewSet(ModelViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = GroupSerializer