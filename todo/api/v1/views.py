from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ...models import Task
from .seializer import TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


'''@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def tasklist(request):
    """ V1 of task list view"""
    if request.method == "GET":
        tasks = Task.objects.all()
        seializer = TaskSerializer(tasks, many=True)
        return Response(seializer.data)
    
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    '''
#---------------------------------------------------------------------------

class TaskList(APIView):
    """V2 of task list view"""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request):
        tasks = Task.objects.all()
        seializer = self.serializer_class(tasks, many=True)
        return Response(seializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
#---------------------------------------------------------------------------
    
'''@api_view(["GET","PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def taskdetail(request, id):
    """ V1 of task detail view"""
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
        return Response({"detail":"task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)'''

#------------------------------------------------------------------------------------------------------

class TaskDetail(APIView):
    """ V2 of task detail view"""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request, id):
        task = get_object_or_404(Task, pk=id, user=request.user)
        serializer = self.serializer_class(task)
        return Response(serializer.data)
    
    def put(self, request,id):
        task = get_object_or_404(Task, pk=id, user=request.user)
        serializer = self.serializer_class(task)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request,id):
        task = get_object_or_404(Task, pk=id, user=request.user)
        task.delete()
        return Response({"detail":"task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)





        
