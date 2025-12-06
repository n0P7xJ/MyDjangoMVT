from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from forum.models import Topic, Community, Post


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create or get admin user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@test.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user (password: admin123)'))
        
        # Create topics
        topics_data = [
            {'name': 'Gaming', 'slug': 'gaming', 'icon': '🎮', 'color': '#7289DA'},
            {'name': 'Technology', 'slug': 'technology', 'icon': '💻', 'color': '#5865F2'},
            {'name': 'Sports', 'slug': 'sports', 'icon': '⚽', 'color': '#57F287'},
            {'name': 'Music', 'slug': 'music', 'icon': '🎵', 'color': '#FEE75C'},
            {'name': 'Movies', 'slug': 'movies', 'icon': '🎬', 'color': '#EB459E'},
        ]
        
        topics = {}
        for topic_data in topics_data:
            topic, created = Topic.objects.get_or_create(
                slug=topic_data['slug'],
                defaults=topic_data
            )
            topics[topic.slug] = topic
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created topic: {topic.name}'))
        
        # Create communities
        communities_data = [
            # Technology
            {'name': 'python', 'description': 'Обговорення мови програмування Python', 'topic': 'technology'},
            {'name': 'javascript', 'description': 'JavaScript та веб-розробка', 'topic': 'technology'},
            {'name': 'reactjs', 'description': 'React.js JavaScript library', 'topic': 'technology'},
            {'name': 'django', 'description': 'Django web framework', 'topic': 'technology'},
            {'name': 'webdev', 'description': 'Веб-розробка та дизайн', 'topic': 'technology'},
            {'name': 'programming', 'description': 'Програмування загалом', 'topic': 'technology'},
            {'name': 'linux', 'description': 'Linux та Open Source', 'topic': 'technology'},
            
            # Gaming
            {'name': 'gaming', 'description': 'Загальні ігрові обговорення', 'topic': 'gaming'},
            {'name': 'pcgaming', 'description': 'PC gaming спільнота', 'topic': 'gaming'},
            {'name': 'playstation', 'description': 'PlayStation консолі та ігри', 'topic': 'gaming'},
            {'name': 'xbox', 'description': 'Xbox консолі та ігри', 'topic': 'gaming'},
            {'name': 'minecraft', 'description': 'Minecraft гра та моди', 'topic': 'gaming'},
            {'name': 'cyberpunk', 'description': 'Cyberpunk 2077', 'topic': 'gaming'},
            
            # Sports
            {'name': 'football', 'description': 'Футбол - обговорення матчів та новин', 'topic': 'sports'},
            {'name': 'basketball', 'description': 'Баскетбол NBA та FIBA', 'topic': 'sports'},
            {'name': 'fitness', 'description': 'Фітнес та здоровий спосіб життя', 'topic': 'sports'},
            {'name': 'cycling', 'description': 'Велоспорт та велопрогулянки', 'topic': 'sports'},
            {'name': 'tennis', 'description': 'Теніс - турніри та обговорення', 'topic': 'sports'},
            
            # Music
            {'name': 'music', 'description': 'Музика всіх жанрів', 'topic': 'music'},
            {'name': 'hiphop', 'description': 'Hip-Hop та рап музика', 'topic': 'music'},
            {'name': 'rock', 'description': 'Рок музика', 'topic': 'music'},
            {'name': 'electronic', 'description': 'Електронна музика', 'topic': 'music'},
            {'name': 'guitar', 'description': 'Гітара - навчання та обговорення', 'topic': 'music'},
            
            # Movies
            {'name': 'movies', 'description': 'Фільми - рецензії та обговорення', 'topic': 'movies'},
            {'name': 'marvel', 'description': 'Marvel всесвіт', 'topic': 'movies'},
            {'name': 'netflix', 'description': 'Netflix серіали та фільми', 'topic': 'movies'},
            {'name': 'anime', 'description': 'Аніме та манга', 'topic': 'movies'},
            {'name': 'starwars', 'description': 'Зоряні Війни', 'topic': 'movies'},
        ]
        
        for comm_data in communities_data:
            topic_slug = comm_data.pop('topic')
            community, created = Community.objects.get_or_create(
                name=comm_data['name'],
                defaults={
                    **comm_data,
                    'created_by': user,
                    'topic': topics[topic_slug]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created community: r/{community.name}'))
        
        # Create sample posts
        communities = Community.objects.all()
        if communities.exists():
            posts_data = [
                {
                    'title': 'Вітаємо в нашій спільноті!',
                    'content': 'Це перший пост в нашій спільноті. Діліться своїми ідеями та обговорюйте цікаві теми!',
                    'post_type': 'text',
                },
                {
                    'title': 'Які ваші улюблені проекти?',
                    'content': 'Поділіться проектами над якими ви працюєте або які вас надихають.',
                    'post_type': 'text',
                },
                {
                    'title': 'Поради для новачків',
                    'content': 'Збираємо найкращі поради та ресурси для тих хто тільки починає.',
                    'post_type': 'text',
                },
            ]
            
            # Створити пости для кожної спільноти
            for community in communities:
                for i, post_data in enumerate(posts_data):
                    # Додати номер до заголовка щоб уникнути дублікатів
                    modified_title = f"{post_data['title']}"
                    if i > 0:
                        modified_title = post_data['title']
                    
                    post, created = Post.objects.get_or_create(
                        title=modified_title,
                        community=community,
                        author=user,
                        defaults={
                            'content': post_data['content'],
                            'post_type': post_data['post_type'],
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'  Created post in r/{community.name}: {modified_title[:50]}'))
        
        self.stdout.write(self.style.SUCCESS('\nSample data created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Communities: {Community.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Topics: {Topic.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Posts: {Post.objects.count()}'))
