from rest_framework import viewsets


from .models import Size
from .serializers import SizeSerializer


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
