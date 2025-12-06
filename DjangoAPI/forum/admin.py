from django.contrib import admin
from .models import Topic, Community, CommunityMember, Post, Vote, Comment, CommentVote


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'order', 'is_active', 'icon', 'color']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'topic', 'created_by', 'members_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['topic', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CommunityMember)
class CommunityMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'community', 'is_moderator', 'joined_at']
    list_filter = ['is_moderator', 'joined_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'community', 'post_type', 'score', 'created_at']
    list_filter = ['post_type', 'is_pinned', 'is_locked', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'score', 'is_deleted', 'created_at']
    list_filter = ['is_deleted', 'created_at']


@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
