from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'
    
class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

class Events(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    places = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.category.name}'
    
class Image(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='images')
    review = models.ForeignKey('EventReviews', on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='images', blank=True)

    def __str__(self):
        return f'Image for {self.event.title}'
    

class EventReviews(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    rating = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.event.title} - {self.rating} stars'


class Answers(models.Model):
    review = models.ForeignKey(EventReviews, on_delete=models.CASCADE)
    answer_text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.answer_text}'