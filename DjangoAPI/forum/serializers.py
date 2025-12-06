from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Topic, Community, CommunityMember, Post, Vote, Comment, CommentVote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']


class TopicSerializer(serializers.ModelSerializer):
    subtopics_count = serializers.SerializerMethodField()
    communities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 
                  'parent', 'order', 'is_active', 'subtopics_count', 'communities_count']
    
    def get_subtopics_count(self, obj):
        return obj.subtopics.filter(is_active=True).count()
    
    def get_communities_count(self, obj):
        return obj.communities.count()


class CommunitySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    is_member = serializers.SerializerMethodField()
    
    class Meta:
        model = Community
        fields = ['id', 'name', 'slug', 'description', 'icon', 'banner', 
                  'created_by', 'created_at', 'members_count', 'is_member']
        read_only_fields = ['slug', 'created_at', 'members_count']
    
    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommunityMember.objects.filter(community=obj, user=request.user).exists()
        return False


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    community = serializers.StringRelatedField()
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'post_type', 'link_url', 
                  'image', 'video_url', 'author', 'community', 'created_at', 'updated_at',
                  'upvotes', 'downvotes', 'score', 'comments_count', 'user_vote',
                  'is_pinned', 'is_locked']
    
    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = Vote.objects.filter(post=obj, user=request.user).first()
            return vote.vote_type if vote else None
        return None


class PostDetailSerializer(PostListSerializer):
    community = CommunitySerializer(read_only=True)
    
    class Meta(PostListSerializer.Meta):
        pass


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type', 'link_url', 'image', 'video_url', 'community']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    user_vote = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'parent', 'created_at',
                  'updated_at', 'upvotes', 'downvotes', 'score', 'user_vote',
                  'is_deleted', 'replies_count']
        read_only_fields = ['author', 'created_at', 'updated_at', 'upvotes', 
                            'downvotes', 'score']
    
    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = CommentVote.objects.filter(comment=obj, user=request.user).first()
            return vote.vote_type if vote else None
        return None
    
    def get_replies_count(self, obj):
        return obj.replies.count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['vote_type']
