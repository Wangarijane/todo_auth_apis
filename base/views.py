from django.shortcuts import render
from base.serializers import UserSerializer, TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from base.models import Todo
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


# Create your views here.

class UserRegistrationView(APIView):
    serializer_class = UserSerializer

    @extend_schema(
            request=UserSerializer
    )

    def post(self, request):
        user = request.user
        print("WHO IS REGISTERING",user)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoListCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoSerializer

    @extend_schema(
        request=TodoSerializer,)
    def get(self, request):
        todo = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        user = request.user
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request, pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
        except Todo.DoesNotExist:
            return Response(data={"detail": "Todo not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TodoSerializer(todo)
        return Response(serializer.data)


    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
        except Todo.DoesNotExist:
            return Response(data={"detail": "Todo not found."}, status=status.HTTP_404_NOT_FOUND)
        
        todo.delete()
        return Response(data={"detail": "Todo record deleted."}, status=status.HTTP_204_NO_CONTENT)