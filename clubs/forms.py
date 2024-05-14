from django import forms
from .models import Club, Event, Announcement, Discussion, Topic, Comment, LeaderProfile, MemberProfile
from .models import Faq, Contact

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'image', 'description']
        
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'venue']
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description']
        
class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['name', 'description']
        
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
class LeaderProfileForm(forms.ModelForm):
    class Meta:
        model = LeaderProfile
        fields = ['bio', 'image']
        
class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['bio', 'image']
        
class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['question', 'answer']
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']