from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Topic(models.Model):
    """Тема/Категорія (як Topics на Reddit)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # emoji or icon name
    color = models.CharField(max_length=7, default='#0079d3')  # hex color
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subtopics')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Community(models.Model):
    """Спільнота (як subreddit)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='communities')
    icon = models.ImageField(upload_to='community_icons/', null=True, blank=True)
    banner = models.ImageField(upload_to='community_banners/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities')
    created_at = models.DateTimeField(auto_now_add=True)
    members_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Communities'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"r/{self.name}"


class CommunityMember(models.Model):
    """Членство в спільноті"""
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined_communities')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_moderator = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('community', 'user')
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} in r/{self.community.name}"


class Post(models.Model):
    """Пост на форумі"""
    LINK = 'link'
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    
    POST_TYPES = [
        (LINK, 'Link'),
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    content = models.TextField(blank=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default=TEXT)
    link_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text='URL відео (YouTube, Vimeo, або пряме посилання)')
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    score = models.IntegerField(default=0)  # upvotes - downvotes
    
    comments_count = models.IntegerField(default=0)
    
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_pinned', '-score', '-created_at']
        indexes = [
            models.Index(fields=['-score', '-created_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:340]
            # Якщо пост новий, спочатку зберігаємо без slug
            if not self.pk:
                # Тимчасовий унікальний slug
                import uuid
                temp_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                self.slug = temp_slug
            else:
                self.slug = f"{base_slug}-{self.pk}"
        
        self.score = self.upvotes - self.downvotes
        super().save(*args, **kwargs)
        
        # Оновлюємо slug з правильним ID після першого збереження
        if self.pk and not self.slug.endswith(str(self.pk)):
            base_slug = slugify(self.title)[:340]
            new_slug = f"{base_slug}-{self.pk}"
            if new_slug != self.slug:
                self.slug = new_slug
                super().save(update_fields=['slug'])
    
    def __str__(self):
        return self.title


class Vote(models.Model):
    """Голосування за пост"""
    UPVOTE = 1
    DOWNVOTE = -1
    
    VOTE_CHOICES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user.username} {'↑' if self.vote_type == self.UPVOTE else '↓'} {self.post.title}"


class Comment(models.Model):
    """Коментар до посту"""
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-score', '-created_at']
    
    def save(self, *args, **kwargs):
        self.score = self.upvotes - self.downvotes
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class CommentVote(models.Model):
    """Голосування за коментар"""
    UPVOTE = 1
    DOWNVOTE = -1
    
    VOTE_CHOICES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'comment')
    
    def __str__(self):
        return f"{self.user.username} {'↑' if self.vote_type == self.UPVOTE else '↓'} comment"
