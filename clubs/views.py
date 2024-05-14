from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Club, Event, Announcement, Discussion, Topic, Comment, LeaderProfile, MemberProfile, Faq, Contact
from .forms import ClubForm, EventForm, AnnouncementForm, DiscussionForm, TopicForm, CommentForm, LeaderProfileForm, MemberProfileForm, FaqForm, ContactForm

from datetime import datetime
# Create your views here.

def member_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid credentials')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.groups.filter(name='member').exists():
                messages.error(request, 'You are not a member')
                return redirect('login')
            if not user.is_active:
                messages.error(request, 'Your account is not activated yet')
                return redirect('login')
            login(request, user)
            request.session['type'] = 'member'
            return redirect('member_profile')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'member_login.html')

def member_register(request):
    info = None
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect('register')
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return redirect('register')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()
        # create group if not exists
        group, created = Group.objects.get_or_create(name='member')
        if created:
            group.save()
        group.user_set.add(user)

        messages.success(request, 'Account created successfully')
        info = "Your account has been created successfully. Your account will be activated by the admin. You will be notified via email."
    return render(request, 'member_register.html', {'info': info})

def leader_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid credentials')
            return redirect('leader_login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.groups.filter(name='leader').exists():
                messages.error(request, 'You are not a leader')
                return redirect('leader_login')
            if not user.is_active:
                messages.error(request, 'Your account is not activated yet')
                return redirect('leader_login')
            login(request, user)
            request.session['type'] = 'leader'
            return redirect('leader_profile')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('leader_login')
    return render(request, 'leader_login.html')

def leader_register(request):
    info = None
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect('register')
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return redirect('register')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()
        # create group if not exists
        group, created = Group.objects.get_or_create(name='leader')
        if created:
            group.save()
        group.user_set.add(user)

        messages.success(request, 'Account created successfully')
        info = "Your account has been created successfully. Your account will be activated by the admin. You will be notified via email."
    return render(request, 'leader_register.html', {'info': info})

def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect('login')

def member_profile(request):
    if request.session['type'] != 'member':
        return redirect('login')
    user = request.user
    if not MemberProfile.objects.filter(user=user).exists():
        return redirect('member_profile_edit')
    profile = MemberProfile.objects.get(user=user)
    clubs = Club.objects.filter(members=user)
    announcements = Announcement.objects.filter(club__members=user)
    events = Event.objects.filter(club__members=user)
    discussions = Discussion.objects.filter(club__members=user)
    return render(request, 'member_profile.html', {'profile': profile, 
                                                   'clubs': clubs, 
                                                   'announcements': announcements, 
                                                   'events': events,
                                                    'discussions': discussions})
    
def member_profile_edit(request):
    if request.session['type'] != 'member':
        return redirect('login')
    user = request.user
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('member_profile')
    else:
        if MemberProfile.objects.filter(user=user).exists():
            profile = MemberProfile.objects.get(user=user)
            form = MemberProfileForm(instance=profile)
        else:
            form = MemberProfileForm()
    return render(request, 'member_profile_edit.html', {'form': form})

def leader_profile(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    if not LeaderProfile.objects.filter(user=user).exists():
        return redirect('leader_profile_edit')
    profile = LeaderProfile.objects.get(user=user)
    clubs = Club.objects.filter(leader=user)
    announcements = Announcement.objects.filter(club__leader=user)
    events = Event.objects.filter(club__leader=user)
    discussions = Discussion.objects.filter(club__leader=user)
    return render(request, 'leader_profile.html', {'profile': profile, 
                                                'clubs': clubs, 
                                                'announcements': announcements, 
                                                'events': events,
                                                'discussions': discussions})
    
def leader_profile_edit(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    if request.method == 'POST':
        form = LeaderProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('leader_profile')
    else:
        if LeaderProfile.objects.filter(user=user).exists():
            profile = LeaderProfile.objects.get(user=user)
            form = LeaderProfileForm(instance=profile)
        else:
            form = LeaderProfileForm()
    return render(request, 'leader_profile_edit.html', {'form': form})

def list_clubs(request):
    clubs = Club.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs})

def search_club(request):
    query = request.GET['query']
    clubs = Club.objects.filter(name__icontains=query)
    return render(request, 'club_list.html', {'clubs': clubs})

def create_club(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.leader = user
            club.save()
            messages.success(request, 'Club created successfully')
            return redirect('list_clubs')
    else:
        form = ClubForm()
    return render(request, 'club_create.html', {'form': form})

def edit_club(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.leader = user
            club.save()
            messages.success(request, 'Club updated successfully')
            return redirect('list_clubs')
    else:
        if Club.objects.filter(leader=user).exists():
            club = Club.objects.get(leader=user)
            form = ClubForm(instance=club)
        else:
            form = ClubForm()
    return render(request, 'club_edit.html', {'form': form})

def remove_club(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    if Club.objects.filter(leader=user).exists():
        club = Club.objects.get(leader=user)
        club.delete()
        messages.success(request, 'Club removed successfully')
    return redirect('list_clubs')

def detail_club(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    return render(request, 'club_detail.html', {'club': club})

def apply_club(request):
    if request.session['type'] != 'member':
        return redirect('login')
    user = request.user
    club_id = request.GET['club_id']
    club = get_object_or_404(Club, pk=club_id)
    club.members.add(user)
    messages.success(request, 'You have applied to the club')
    return redirect('list_clubs')

def leave_club(request):
    if request.session['type'] != 'member':
        return redirect('login')
    user = request.user
    club_id = request.GET['club_id']
    club = get_object_or_404(Club, pk=club_id)
    club.members.remove(user)
    messages.success(request, 'You have left the club')
    return redirect('list_clubs')

def accept_club(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    club_id = request.GET['club_id']
    member_id = request.GET['member_id']
    club = get_object_or_404(Club, pk=club_id)
    member = get_object_or_404(User, pk=member_id)
    club.members.add(member)
    messages.success(request, 'Member accepted successfully')
    return redirect('detail_club', club_id)

def reject_club(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    club_id = request.GET['club_id']
    member_id = request.GET['member_id']
    club = get_object_or_404(Club, pk=club_id)
    member = get_object_or_404(User, pk=member_id)
    club.members.remove(member)
    messages.success(request, 'Member rejected successfully')
    return redirect('detail_club', club_id)

def create_event(request, cid):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    club = get_object_or_404(Club, pk=cid)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club
            event.save()
            messages.success(request, 'Event created successfully')
            return redirect('list_events', cid)
    else:
        form = EventForm()
    return render(request, 'event_create.html', {'form': form, 'club': club})

def edit_event(request, eid):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    event = get_object_or_404(Event, pk=eid)
    club = event.club
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club
            event.save()
            messages.success(request, 'Event updated successfully')
            return redirect('list_events', club.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'event_edit.html', {'form': form, 'club': club})

def detail_event(request, eid):
    event = get_object_or_404(Event, pk=eid)
    return render(request, 'event_detail.html', {'event': event})

def list_events(request, cid):
    club = get_object_or_404(Club, pk=cid)
    events = Event.objects.filter(club=club)
    return render(request, 'event_list.html', {'events': events, 'club': club})

def remove_event(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    event_id = request.GET['event_id']
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    messages.success(request, 'Event removed successfully')
    return redirect('list_events', event.club.id)

def join_event(request):
    if request.session['type'] != 'member':
        return redirect('login')
    user = request.user
    event_id = request.GET['event_id']
    event = get_object_or_404(Event, pk=event_id)
    event.members.add(user)
    messages.success(request, 'You have joined the event')
    return redirect('list_events', event.club.id)

def leave_event(request):
    if request.session['type'] != 'member':
        return redirect('login')
    user = request.user
    event_id = request.GET['event_id']
    event = get_object_or_404(Event, pk=event_id)
    event.members.remove(user)
    messages.success(request, 'You have left the event')
    return redirect('list_events', event.club.id)

def create_announcement(request, cid):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    club = get_object_or_404(Club, pk=cid)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.club = club
            announcement.save()
            messages.success(request, 'Announcement created successfully')
            return redirect('list_announcements', cid)
    else:
        form = AnnouncementForm()
    return render(request, 'ann_create.html', {'form': form, 'club': club})

def edit_announcement(request, aid):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    announcement = get_object_or_404(Announcement, pk=aid)
    club = announcement.club
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.club = club
            announcement.save()
            messages.success(request, 'Announcement updated successfully')
            return redirect('list_announcements', club.id)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'ann_edit.html', {'form': form, 'club': club})

def detail_announcement(request, aid):
    announcement = get_object_or_404(Announcement, pk=aid)
    return render(request, 'ann_detail.html', {'announcement': announcement})

def list_announcements(request, cid):
    club = get_object_or_404(Club, pk=cid)
    announcements = Announcement.objects.filter(club=club)
    return render(request, 'ann_list.html', {'announcements': announcements, 'club': club})

def delete_announcement(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    announcement_id = request.GET['announcement_id']
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    announcement.delete()
    messages.success(request, 'Announcement removed successfully')
    return redirect('list_announcements', announcement.club.id)

def create_discussion(request, cid):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    club = get_object_or_404(Club, pk=cid)
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.club = club
            discussion.save()
            messages.success(request, 'Discussion created successfully')
            return redirect('list_discussions', cid)
    else:
        form = DiscussionForm()
    return render(request, 'dis_create.html', {'form': form, 'club': club})

def edit_discussion(request, did):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    discussion = get_object_or_404(Discussion, pk=did)
    club = discussion.club
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.club = club
            discussion.save()
            messages.success(request, 'Discussion updated successfully')
            return redirect('list_discussions', club.id)
    else:
        form = DiscussionForm(instance=discussion)
    return render(request, 'dis_edit.html', {'form': form, 'club': club})

def detail_discussion(request, did):
    discussion = get_object_or_404(Discussion, pk=did)
    return render(request, 'dis_detail.html', {'discussion': discussion})

def list_discussions(request, cid):
    club = get_object_or_404(Club, pk=cid)
    discussions = Discussion.objects.filter(club=club)
    return render(request, 'dis_list.html', {'discussions': discussions, 'club': club})

def remove_discussion(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    discussion_id = request.GET['discussion_id']
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    discussion.delete()
    messages.success(request, 'Discussion removed successfully')
    return redirect('list_discussions', discussion.club.id)

def join_discussion(request):
    if request.session['type'] != 'member':
        return redirect('login')
    user = request.user
    discussion_id = request.GET['discussion_id']
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    discussion.members.add(user)
    messages.success(request, 'You have joined the discussion')
    return redirect('list_discussions', discussion.club.id)

def leave_discussion(request):
    if request.session['type'] != 'member':
        return redirect('login')
    user = request.user
    discussion_id = request.GET['discussion_id']
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    discussion.members.remove(user)
    messages.success(request, 'You have left the discussion')
    return redirect('list_discussions', discussion.club.id)

def faq(request):
    faqs = Faq.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, 'Your message has been sent successfully')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def create_topic(request, did):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    discussion = get_object_or_404(Discussion, pk=did)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.discussion = discussion
            topic.save()
            messages.success(request, 'Topic created successfully')
            return redirect('list_topics', did)
    else:
        form = TopicForm()
    return render(request, 'topic_create.html', {'form': form, 'discussion': discussion})


def edit_topic(request, tid):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    topic = get_object_or_404(Topic, pk=tid)
    discussion = topic.discussion
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.discussion = discussion
            topic.save()
            messages.success(request, 'Topic updated successfully')
            return redirect('list_topics', discussion.id)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'topic_edit.html', {'form': form, 'discussion': discussion})

def detail_topic(request, tid):
    topic = get_object_or_404(Topic, pk=tid)
    comments = Comment.objects.filter(topic=topic)
    return render(request, 'topic_detail.html', {'topic': topic, 'comments': comments})

def list_topics(request, did):
    discussion = get_object_or_404(Discussion, pk=did)
    topics = Topic.objects.filter(discussion=discussion)
    return render(request, 'topic_list.html', {'topics': topics, 'discussion': discussion})

def remove_topic(request):
    if request.session['type'] != 'leader':
        return redirect('leader_login')
    user = request.user
    topic_id = request.GET['topic_id']
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.delete()
    messages.success(request, 'Topic removed successfully')
    return redirect('list_topics', topic.discussion.id)

def create_comment(request, tid):
    if request.session['type'] != 'member':
        return redirect('login')
    user = request.user
    topic = get_object_or_404(Topic, pk=tid)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.user = user
            comment.save()
            messages.success(request, 'Comment created successfully')
    return redirect('detail_topic', tid)

def edit_comment(request, cid):
    if request.session['type'] != 'member':
        return redirect('login')
    user = request.user
    comment = get_object_or_404(Comment, pk=cid)
    topic = comment.topic
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.user = user
            comment.save()
            messages.success(request, 'Comment updated successfully')
    return redirect('detail_topic', topic.id)
        
def home(request):
    clubs = Club.objects.all()
    return render(request, 'home.html', {'clubs': clubs})



