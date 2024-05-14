from django.db import models
from django.contrib.auth.models import User, Group

class Event(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event_images/')
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=100)
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='attendees')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Discussion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    discussion = models.ForeignKey('Discussion', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    text = models.TextField()
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text

class Club(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='club_images/')
    description = models.TextField()
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader', null=True, blank=True)
    members = models.ManyToManyField(User, related_name='members')
    events = models.ManyToManyField('Event', related_name='events')
    announcements = models.ManyToManyField('Announcement', related_name='announcements')
    discussions = models.ManyToManyField('Discussion', related_name='discussions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class LeaderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='leader_images/')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='member_images/')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Faq(models.Model):
    question = models.CharField(max_length=100)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    
