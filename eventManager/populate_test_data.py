import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventManager.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from accounts.models import Categories, Events, EventReviews, Answers, Tags, Image

def populate_test_data():
    # Utilisateurs
    user1, _ = User.objects.get_or_create(
        username='alice', defaults={'email': 'alice@example.com'}
    )
    user2, _ = User.objects.get_or_create(
        username='bob', defaults={'email': 'bob@example.com'}
    )

    # Catégories
    cat1, _ = Categories.objects.get_or_create(name='Conférence')
    cat2, _ = Categories.objects.get_or_create(name='Atelier')

    # Tags
    tag_tech, _ = Tags.objects.get_or_create(name='Tech')
    tag_network, _ = Tags.objects.get_or_create(name='Networking')
    tag_ai, _ = Tags.objects.get_or_create(name='AI')
    tag_python, _ = Tags.objects.get_or_create(name='Python')

    # Dates d'événements (futures) pour respecter DateTimeField
    event1_date = timezone.now() + timedelta(days=30)
    event2_date = timezone.now() + timedelta(days=60)

    # Événements (utiliser defaults pour idempotence)
    event1, _ = Events.objects.get_or_create(
        title='DjangoCon 2025',
        defaults={
            'category': cat1,
            'date': event1_date,
            'location': 'Paris',
            'places': 100,
            'created_by': user1,
        },
    )
    event2, _ = Events.objects.get_or_create(
        title='Atelier Python',
        defaults={
            'category': cat2,
            'date': event2_date,
            'location': 'Lyon',
            'places': 50,
            'created_by': user2,
        },
    )

    # Avis
    review1, _ = EventReviews.objects.get_or_create(
        event=event1,
        created_by=user2,
        defaults={'review_text': 'Super conférence, très enrichissante !', 'rating': 5},
    )
    review2, _ = EventReviews.objects.get_or_create(
        event=event2,
        created_by=user1,
        defaults={'review_text': "Atelier intéressant mais un peu court.", 'rating': 4},
    )

    # Réponses aux avis
    Answers.objects.get_or_create(
        review=review1,
        created_by=user1,
        defaults={'answer_text': 'Merci pour votre retour !'},
    )
    Answers.objects.get_or_create(
        review=review2,
        created_by=user2,
        defaults={'answer_text': 'Merci pour votre participation !'},
    )

    # Images liées aux événements et aux avis
    img1, _ = Image.objects.get_or_create(
        event=event1,
        review=None,
        imagePath='images/djangocon.jpg',
    )
    img1.tags.add(tag_tech, tag_python)

    img2, _ = Image.objects.get_or_create(
        event=event2,
        review=None,
        imagePath='images/atelier-python.jpg',
    )
    img2.tags.add(tag_python, tag_network)

    # Images associées aux avis
    img_review1, _ = Image.objects.get_or_create(
        event=event1,
        review=review1,
        imagePath='images/review-djangocon.jpg',
    )
    img_review1.tags.add(tag_ai)

    img_review2, _ = Image.objects.get_or_create(
        event=event2,
        review=review2,
        imagePath='images/review-atelier.jpg',
    )
    img_review2.tags.add(tag_network)

    print("Données de test insérées avec succès.")

if __name__ == '__main__':
    populate_test_data()