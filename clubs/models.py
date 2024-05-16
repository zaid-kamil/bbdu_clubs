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
    attendees = models.ManyToManyField(User, related_name='attendees', null=True, blank=True)
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

class LikeAnnouncement(models.Model):
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE, related_name='announcement')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    



class Discussion(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  
    name = models.CharField(max_length=100)
    description = models.TextField()
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='members', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Topic(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    name = models.CharField(max_length=100)
    description = models.TextField()
    discussion = models.ForeignKey('Discussion', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text

class Club(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='club_images/')
    description = models.TextField()
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader', null=True, blank=True)
    members = models.ManyToManyField(User, related_name='clubmembers', null=True, blank=True)
    events = models.ManyToManyField('Event', related_name='events', null=True, blank=True)
    announcements = models.ManyToManyField('Announcement', related_name='announcements', null=True, blank=True)
    discussions = models.ManyToManyField('Discussion', related_name='discussions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ClubApplication(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} applied for {self.club.name}'

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
    course = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    rollno = models.CharField(max_length=100)
    interest = models.CharField(max_length=100)
    
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
    
    
