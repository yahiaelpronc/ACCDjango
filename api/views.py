from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
# Create your views here.


# @api_view(['GET'])
# def apiOverview(request):
#     api_urls = {
#         'List': '/task-list/',
#         'Detail View': '/task-detail/<str:pk>',
#     }
#     return Response(api_urls)

@api_view(['POST'])
def insertuser(request):
    mydata=UsersSerializer(data=request.data)
    if(mydata.is_valid()):
        mydata.save()
        print(mydata.data)
        return Response(mydata.data)


@api_view(['GET'])
def usersList(request):
    users = Myuser.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUser(request, username):
    user = Myuser.objects.get(username=username)
    serializer = UsersSerializer(user)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteUser(request, username):
    user = Myuser.objects.get(username=username)
    user.delete()
    return Response('Item Successfully Deleted')


# @api_view(['GET'])
# def taskDetail(request, pk):
#     tasks = Task.objects.get(id=pk)
#     serializer = TaskSerializer(tasks, many=False)
#     return Response(serializer.data)


# @api_view(['POST'])
# def taskCreate(request):
#     serializer = TaskSerializer(data=request.data)
#     if(serializer.is_valid()):
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['POST'])
# def taskUpdate(request, pk):
#     task = Task.objects.get(id=pk)
#     serializer = TaskSerializer(instance=task, data=request.data)
#     if(serializer.is_valid()):
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['DELETE'])
# def taskDelete(request, pk):
#     task = Task.objects.get(id=pk)
#     task.delete()
#     return Response('Item Successfully Deleted')
