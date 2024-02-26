from rest_framework.response import Response
from rest_framework import generics
from apps.script.models import Script
from apps.script.apis.serializers import ScriptSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ScriptView(generics.ListCreateAPIView):
    serializer_class = ScriptSerializer
    queryset = Script.objects.all()

    @swagger_auto_schema(
        operation_description="Retrieve a list of scripts.",
        responses={200: ScriptSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="This Api is Used to Create a New Script",
        response={200: ScriptSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ScriptDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = ScriptSerializer
    queryset = Script.objects.all()

    @swagger_auto_schema(
        operation_description="Retrieve a single script detail. You need to pass the Appropriate Script Id",
        responses={200: ScriptSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Updating a single script",
        responses={200: ScriptSerializer(many=True)}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="This Api is used to delete the Script.",
        responses={200: ScriptSerializer(many=True)}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
