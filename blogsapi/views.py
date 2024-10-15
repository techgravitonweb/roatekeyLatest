from django.shortcuts import render
from .models import Blogs
from .serializers import BlogsSerializer
from rest_framework import viewsets


# Create your views here.


class BlogsView(viewsets.ModelViewSet):
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
