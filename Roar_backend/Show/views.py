from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import ShowSerializer, ShowGeneralSerializer
from .models import ShowInfo
from rest_framework.decorators import action


# Create your views here.
class ShowViewSet(viewsets.ModelViewSet):
    queryset = ShowInfo.objects.all()
    serializer_class = ShowGeneralSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    # def get_serializer(self, *args, **kwargs):
    #     if self.action == "list":
    #         return ShowGeneralSerializer(*args, **kwargs)
    #     return super().get_serializer(*args, **kwargs)

