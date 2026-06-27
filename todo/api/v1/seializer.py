from rest_framework import serializers
from ...models import Task

class TaskSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    user = serializers.CharField(source= "username")
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["user"]

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("absolute_url")
        return rep
    
    def create(self, validated_data):
        validated_data["user"] = Task.objects.get(user__id = self.context.get("request").user.id)
    
