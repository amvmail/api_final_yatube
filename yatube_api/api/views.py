from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from .permissions import OwnerOrReadOnly, ReadOnly
from posts.models import Comment, Follow, Post, Group
from .serializers import (CommentSerializer, FollowSerializer, PostSerializer,
                          GroupSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """Viewset к постам."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # применю в этом View для примера разрешения из моего permissions
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('text', 'author', 'group', 'pub_date',)
    search_fields = ('text', 'author__username',)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset к группам."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """"Viewset к комментариям."""
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # pagination_class = None

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        new_queryset = Comment.objects.filter(post_id=post_id)
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужих данных запрещено')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Изменение чужих данных запрещено')
        super(CommentViewSet, self).perform_destroy(instance)


class APIFollowList(generics.ListCreateAPIView):
    """Viewset к подпискам."""
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
