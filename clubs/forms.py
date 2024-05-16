from django import forms
from .models import Club, Event, Announcement, Discussion, Topic, Comment, LeaderProfile, MemberProfile
from .models import Faq, Contact


class LeaderLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class MemberLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class LeaderRegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    name = forms.CharField()
    phone = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    country = forms.CharField()
    pincode = forms.CharField()
    dob = forms.DateField()
    image = forms.ImageField()
    
class MemberRegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    course = forms.CharField()
    semester = forms.CharField()
    rollno = forms.CharField()
    interest = forms.CharField()
    email = forms.EmailField()
    name = forms.CharField()
    phone = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    country = forms.CharField()
    pincode = forms.CharField()
    dob = forms.DateField()
    image = forms.ImageField()
    


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'image', 'description']
        
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['image', 'name', 'description', 'venue', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'venue': forms.TextInput(attrs={'placeholder': 'Enter the venue'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter the name of the event'}),
        }
        
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
        fields ='__all__'
        exclude = ['user']
        
class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = '__all__'
        exclude = ['user']
        
class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['question', 'answer']
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']