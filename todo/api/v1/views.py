from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ...models import Task
from .seializer import TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def tasklist(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        seializer = TaskSerializer(tasks, many=True)
        return Response(seializer.data)
    
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
@api_view(["GET","PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def taskdetail(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    elif request.method=="PUT":
        serializer = TaskSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        task.delete()
        return Response({"detail":"task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        
        
