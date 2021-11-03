from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment
from rest_framework import status
from rest_framework.response import Response


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (AllowAny,)


    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)


class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.all().order_by('id')[0:2]
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)

    def perform_destroy(self, instance):
        instance = self.get_object()

        if not self.request.user == instance.userPost:
            response = {'message': 'Delete is not allowed !'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)

    def perform_destroy(self, instance):
        instance = self.get_object()

        if not self.request.user == instance.userComment:
            response = {'message': 'Delete is not allowed !'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            instance.delete()
