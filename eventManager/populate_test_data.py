import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventManager.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Categories, Events, EventReviews, Answers

def populate_test_data():
    user1, _ = User.objects.get_or_create(username='alice', defaults={'email': 'alice@example.com'})
    user2, _ = User.objects.get_or_create(username='bob', defaults={'email': 'bob@example.com'})

    cat1, _ = Categories.objects.get_or_create(name='Conférence')
    cat2, _ = Categories.objects.get_or_create(name='Atelier')

    event1, _ = Events.objects.get_or_create(
        title='DjangoCon 2025',
        category=cat1,
        date='2025-11-10',
        location='Paris',
        places=100,
        created_by=user1
    )
    event2, _ = Events.objects.get_or_create(
        title='Atelier Python',
        category=cat2,
        date='2025-12-05',
        location='Lyon',
        places=50,
        created_by=user2
    )

    EventReviews.objects.get_or_create(
        event=event1,
        review_text='Super conférence, très enrichissante !',
        rating=5,
        created_by=user2
    )
    EventReviews.objects.get_or_create(
        event=event2,
        review_text='Atelier intéressant mais un peu court.',
        rating=4,
        created_by=user1
    )

    # Création de réponses aux avis
    review1 = EventReviews.objects.get(event=event1, created_by=user2)
    review2 = EventReviews.objects.get(event=event2, created_by=user1)

    Answers.objects.get_or_create(
        review=review1,
        answer_text="Merci pour votre retour !",
        created_by=user1
    )
    Answers.objects.get_or_create(
        review=review2,
        answer_text="Merci pour votre participation !",
        created_by=user2
    )

    print("Données de test insérées avec succès.")

if __name__ == '__main__':
    populate_test_data()