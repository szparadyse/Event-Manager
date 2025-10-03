from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Answers, Categories, EventReviews, Events, Image

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:login')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Events.objects.order_by('date')[:5]  # Les 5 prochains événements
        context['categories'] = Categories.objects.all()
        return context


def event_reviews(request, event_id):
    reviews = EventReviews.objects.filter(event_id=event_id)
    return render(request, 'event_reviews.html', {'reviews': reviews})

def event_list(request):
    events = Events.objects.all()
    return render(request, 'event_list.html', {'events': events})

def event_details(request, event_id):
    event = Events.objects.get(id=event_id)
    reviews = EventReviews.objects.filter(event_id=event_id)
    return render(request, 'event_details.html', {'event': event, 'reviews': reviews})

def add_event(request):
    categories = Categories.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        date = request.POST.get('date')
        location = request.POST.get('location')
        places = request.POST.get('places')
        event = Events.objects.create(
            title=title,
            category_id=category_id,
            date=date,
            location=location,
            places=places,
            created_by=request.user
        )
        add_image(request, event_id=event.id)
        return redirect('home')
    return render(request, 'add_event.html', {'categories': categories})

def add_answer(request, review_id):
    if request.method == 'POST':
        answer_text = request.POST.get('answer_text')
        review = EventReviews.objects.get(id=review_id)
        Answers.objects.create(
            review=review,
            answer_text=answer_text,
            created_by=request.user
        )
        return redirect('accounts:event_details', event_id=review.event.id)
    return render(request, 'add_answer.html', {'review_id': review_id})

def add_review(request, event_id):
    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')
        event = Events.objects.get(id=event_id)
        EventReviews.objects.create(
            event=event,
            review_text=review_text,
            rating=rating,
            created_by=request.user
        )
        return redirect('accounts:event_details', event_id=event_id)
    return render(request, 'add_review.html')

def add_image(request, event_id=None, review_id=None):
    if request.method == 'POST':
        imagePath = request.POST.get('imagePath')
        if event_id:
            event = Events.objects.get(id=event_id)
            Image.objects.create(
                event=event,
                imagePath=imagePath
            )
            return redirect('accounts:event_details', event_id=event_id)
        elif review_id:
            review = EventReviews.objects.get(id=review_id)
            Image.objects.create(
                review=review,
                imagePath=imagePath
            )
            return redirect('accounts:event_details', event_id=review.event.id)
    return render(request, 'add_image.html', {'event_id': event_id, 'review_id': review_id})

def category_list(request):
    categories = Categories.objects.all()
    return render(request, 'category_list.html', {'categories': categories})