from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.filters import SearchFilter, OrderingFilter

from news.models import News, Comment, Status, NewsStatus, CommentStatus
from news.paginations import PostPagePagination
from news.permissions import PostPermission
from news.serializers import NewsSerializer, CommentSerializer, StatusSerializer, NewsStatusSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    API для создания, получения, изменения и удаления новостей
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    permission_classes = [PostPermission, ]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', ]
    ordering_fields = ['created_at', ]
    pagination_class = PostPagePagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    API для создания, получения списка комментариев к новостям
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news_id=self.kwargs.get('news_id')
        )


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API детального просмотра, изменения и удаления комментариев
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [PostPermission, permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news_id=self.kwargs.get('news_id')
        )


class StatusViewSet(viewsets.ModelViewSet):
    """
    API для создания типов оценок
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    permission_classes = [permissions.IsAdminUser, ]


@permission_classes(permissions.IsAuthenticated)
@api_view(['GET'])
def status_news(request, news_id, slug):
    my_status = Status.objects.get(slug=slug)
    try:
        NewsStatus.objects.create(news_id=news_id, status=my_status, author=request.user.author)
    except:
        return Response({'error': "You already added status"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Status added'}, status=status.HTTP_201_CREATED)


@permission_classes(permissions.IsAuthenticated)
@api_view(['GET'])
def status_comment(request, news_id, comment_id, slug):
    my_status = Status.objects.get(slug=slug)
    try:
        CommentStatus.objects.create(comment_id=comment_id, status=my_status, author=request.user.author)
    except:
        return Response({'error': "You already added status"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Status added'}, status=status.HTTP_201_CREATED)

