from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import Task
from .seializer import TaskSerializer

@api_view()
def postlist(request):

    Tasks = Task.objects.all()
    seializer = TaskSerializer(Tasks, many=True)
    return Response(seializer.data)
