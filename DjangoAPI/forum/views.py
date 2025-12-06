from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from .models import Topic, Community, CommunityMember, Post, Vote, Comment, CommentVote
from .serializers import (
    TopicSerializer, CommunitySerializer, PostListSerializer, PostDetailSerializer,
    PostCreateSerializer, CommentSerializer, VoteSerializer
)


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для Topics з можливістю фільтрації по parent
    """
    queryset = Topic.objects.filter(is_active=True)
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фільтр по parent - якщо parent=null, повертає тільки головні теми
        parent = self.request.query_params.get('parent', None)
        if parent is not None:
            if parent.lower() == 'null' or parent == '':
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent__slug=parent)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def communities(self, request, slug=None):
        """Отримати всі спільноти для даної теми"""
        topic = self.get_object()
        communities = Community.objects.filter(topic=topic)
        serializer = CommunitySerializer(communities, many=True, context={'request': request})
        return Response(serializer.data)


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'members_count']
    
    def perform_create(self, serializer):
        community = serializer.save(created_by=self.request.user)
        # Автоматично додати створювача як модератора
        CommunityMember.objects.create(
            community=community,
            user=self.request.user,
            is_moderator=True
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, slug=None):
        community = self.get_object()
        member, created = CommunityMember.objects.get_or_create(
            community=community,
            user=request.user
        )
        if created:
            Community.objects.filter(id=community.id).update(members_count=F('members_count') + 1)
            return Response({'message': 'Joined successfully'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Already a member'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def leave(self, request, slug=None):
        community = self.get_object()
        deleted = CommunityMember.objects.filter(community=community, user=request.user).delete()[0]
        if deleted:
            Community.objects.filter(id=community.id).update(members_count=F('members_count') - 1)
            return Response({'message': 'Left successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Not a member'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        community = self.get_object()
        posts = Post.objects.filter(community=community)
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'community').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'score', 'comments_count']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        community_slug = self.request.query_params.get('community', None)
        if community_slug:
            queryset = queryset.filter(community__slug=community_slug)
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, slug=None):
        post = self.get_object()
        vote_type = request.data.get('vote_type')
        
        if vote_type not in [Vote.UPVOTE, Vote.DOWNVOTE]:
            return Response({'error': 'Invalid vote type'}, status=status.HTTP_400_BAD_REQUEST)
        
        vote, created = Vote.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={'vote_type': vote_type}
        )
        
        # Оновити лічильники
        upvotes = Vote.objects.filter(post=post, vote_type=Vote.UPVOTE).count()
        downvotes = Vote.objects.filter(post=post, vote_type=Vote.DOWNVOTE).count()
        Post.objects.filter(id=post.id).update(upvotes=upvotes, downvotes=downvotes, score=upvotes-downvotes)
        
        return Response({'message': 'Voted successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unvote(self, request, slug=None):
        post = self.get_object()
        deleted = Vote.objects.filter(user=request.user, post=post).delete()[0]
        
        if deleted:
            upvotes = Vote.objects.filter(post=post, vote_type=Vote.UPVOTE).count()
            downvotes = Vote.objects.filter(post=post, vote_type=Vote.DOWNVOTE).count()
            Post.objects.filter(id=post.id).update(upvotes=upvotes, downvotes=downvotes, score=upvotes-downvotes)
            return Response({'message': 'Vote removed'}, status=status.HTTP_200_OK)
        return Response({'message': 'No vote to remove'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, slug=None):
        post = self.get_object()
        # Отримати тільки кореневі коментарі (без parent)
        comments = Comment.objects.filter(post=post, parent=None)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        post_slug = self.request.query_params.get('post', None)
        parent_id = self.request.query_params.get('parent', None)
        
        if post_slug:
            queryset = queryset.filter(post__slug=post_slug)
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        
        return queryset
    
    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Оновити лічильник коментарів
        Post.objects.filter(id=comment.post.id).update(comments_count=F('comments_count') + 1)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        comment = self.get_object()
        vote_type = request.data.get('vote_type')
        
        if vote_type not in [CommentVote.UPVOTE, CommentVote.DOWNVOTE]:
            return Response({'error': 'Invalid vote type'}, status=status.HTTP_400_BAD_REQUEST)
        
        vote, created = CommentVote.objects.update_or_create(
            user=request.user,
            comment=comment,
            defaults={'vote_type': vote_type}
        )
        
        # Оновити лічильники
        upvotes = CommentVote.objects.filter(comment=comment, vote_type=CommentVote.UPVOTE).count()
        downvotes = CommentVote.objects.filter(comment=comment, vote_type=CommentVote.DOWNVOTE).count()
        Comment.objects.filter(id=comment.id).update(upvotes=upvotes, downvotes=downvotes, score=upvotes-downvotes)
        
        return Response({'message': 'Voted successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        comment = self.get_object()
        replies = Comment.objects.filter(parent=comment)
        serializer = CommentSerializer(replies, many=True, context={'request': request})
        return Response(serializer.data)
