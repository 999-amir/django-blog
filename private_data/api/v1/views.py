from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from private_data.models import PrivateDataModel
from .permissions import IsVerify
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import PrivateDataPaginator


class PrivateDataAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsVerify]
    serializer_class = PrivateDataSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', '$title', 'created', 'updated']
    ordering_fields = ['created', 'updated']
    pagination_class = PrivateDataPaginator

    def get_queryset(self):
        queryset = PrivateDataModel.objects.filter(user=self.request.user)
        return queryset
