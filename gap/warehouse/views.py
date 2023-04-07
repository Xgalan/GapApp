from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

from core.views import StandardResultsSetPagination
from warehouse.models import Storage
from warehouse.serializers import StorageSerializer


class StorageViewSet(ModelViewSet):
    """
    API endpoint that allows partnumbers to be viewed or edited.
    """

    queryset = Storage.objects.prefetch_related("items").all()
    serializer_class = StorageSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    renderer_classes = [
        JSONRenderer,
    ]
