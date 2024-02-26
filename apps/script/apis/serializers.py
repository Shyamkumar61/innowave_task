import re
from rest_framework import serializers
from apps.script.models import Script


class ScriptSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = Script
        fields = ('name', 'category', 'owner', 'status')

    def validate_name(self, attrs):
        if not attrs:
            raise serializers.ValidationError("Name Cannot be Empty. Please Enter the name of Script")
        if attrs and not re.match(r'^[a-zA-Z\s]*$', attrs):
            raise serializers.ValidationError("Name Cannot Contain Numbers and Special Letters")
        return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['owner'] = instance.owner.first_name
        return response
