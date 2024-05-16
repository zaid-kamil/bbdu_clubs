from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Club, Event, Announcement, Discussion, Topic, Comment, LeaderProfile, MemberProfile, Faq, Contact, ClubApplication
from .forms import ClubForm, EventForm, AnnouncementForm, DiscussionForm, TopicForm, CommentForm, LeaderProfileForm, MemberProfileForm, FaqForm, ContactForm
from .forms import LeaderLoginForm, MemberLoginForm, LeaderRegistrationForm, MemberRegistrationForm
from datetime import datetime
# Create your views here.



def member_login(request):
    form = MemberLoginForm()
    if request.method == 'POST':
        form = MemberLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
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
                request.session['is_member'] = True
                return redirect('member_profile')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('login')
    return render(request, 'member_login.html', {'form': form})

def member_register(request):
    info = None
    form = MemberRegistrationForm()
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            name = request.POST['name']
            phone = request.POST['phone']
            address = request.POST['address']
            course = request.POST['course']
            semester = request.POST['semester']
            rollno = request.POST['rollno']
            interest = request.POST['interest']
            city = request.POST['city']
            state = request.POST['state']
            address = request.POST['address']
            country = request.POST['country']
            pincode = request.POST['pincode']
            dob = request.POST['dob']
            image = request.FILES['image']
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
            if len(phone) != 10 and not phone.isdigit():
                messages.error(request, 'Phone number must be 10 digits')
                return redirect('register')
            if len(pincode) != 6:
                messages.error(request, 'Pincode must be 6 digits')
                return redirect('register')
            if len(rollno) < 1:
                messages.error(request, 'Roll number is required')
                return redirect('register')
            if len(interest) < 1:
                messages.error(request, 'Interest is required')
                return redirect('register')
            if len(course) < 1:
                messages.error(request, 'Course is required')
                return redirect('register')
            if len(semester) < 1:
                messages.error(request, 'Semester is required')
                return redirect('register')
            if len(dob) < 1:
                messages.error(request, 'Date of birth is required')
                return redirect('register')
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()
            # create group if not exists
            group, created = Group.objects.get_or_create(name='member')
            if created:
                group.save()
            group.user_set.add(user)
            # create member profile
            dob = datetime.strptime(dob, '%d/%m/%Y').strftime('%Y-%m-%d')
            print(dob)
            profile = MemberProfile(user=user, 
                                    image=image,
                                    name=name, 
                                    email=email, 
                                    phone=phone, 
                                    address=address, 
                                    city=city, 
                                    state=state, 
                                    country=country, 
                                    pincode=pincode, 
                                    dob=dob, 
                                    course=course, 
                                    semester=semester, 
                                    rollno=rollno, 
                                    interest=interest, 
                                    )
            profile.save()

            messages.success(request, 'Account created successfully')
            info = "Your account has been created successfully. Your account will be activated by the admin. You will be notified via email."
    return render(request, 'member_register.html', {'info': info, 'form': form})

def leader_login(request):
    form = LeaderLoginForm()
    if request.method == 'POST':
        form = LeaderLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
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
                request.session['is_leader'] = True
                return redirect('leader_profile')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('leader_login')
    return render(request, 'leader_login.html', {'form': form})

def leader_register(request):
    info = None
    form = LeaderRegistrationForm()
    if request.method == 'POST':
        form = LeaderRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            pincode = form.cleaned_data['pincode']
            dob = form.cleaned_data['dob']
            image = form.cleaned_data['image']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('leader_register')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken')
                return redirect('leader_register')
            if len(password) < 6:
                messages.error(request, 'Password must be at least 6 characters')
                return redirect('leader_register')
            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return redirect('leader_register')
            if len(phone) != 10 and not phone.isdigit():
                messages.error(request, 'Phone number must be 10 digits')
                return redirect('leader_register')
            if len(pincode) != 6:
                messages.error(request, 'Pincode must be 6 digits')
                return redirect('leader_register')
            if len(dob) < 1:
                messages.error(request, 'Date of birth is required')
                return redirect('leader_register')
            if len(name) < 1:
                messages.error(request, 'Name is required')
                return redirect('leader_register')
            if len(address) < 1:
                messages.error(request, 'Address is required')
                return redirect('leader_register')
            if len(city) < 1:
                messages.error(request, 'City is required')
                return redirect('leader_register')
            if len(state) < 1:
                messages.error(request, 'State is required')
                return redirect('leader_register')
            if len(country) < 1:
                messages.error(request, 'Country is required')
                return redirect('leader_register')
            if len(pincode) < 1:
                messages.error(request, 'Pincode is required')
                return redirect('leader_register')
            if len(dob) < 1:
                messages.error(request, 'Date of birth is required')
                return redirect('leader_register')

            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()
            # create group if not exists
            group, created = Group.objects.get_or_create(name='leader')
            if created:
                group.save()
            group.user_set.add(user)
            # create leader profile
            # convert dob to yyyy-mm-dd format from 'dd/mm/yyyy' str
            # dob = datetime.strptime(dob, '%d/%m/%Y').strftime('%Y-%m-%d')
            print(dob)
            profile = LeaderProfile(user=user, 
                                    image=image,
                                    name=name, 
                                    email=email, 
                                    phone=phone, 
                                    address=address, 
                                    city=city, 
                                    state=state, 
                                    country=country, 
                                    pincode=pincode, 
                                    dob=dob, 
                                    )
            profile.save()

            messages.success(request, 'Account created successfully')
            info = "Your account has been created successfully. Your account will be activated by the admin. You will be notified via email."
    return render(request, 'leader_register.html', {'info': info, 'form': form})

def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect('home')

@login_required
def member_profile(request):
    if 'type' in request.session and request.session.get('type') != 'member':
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
    
@login_required
def member_profile_edit(request):
    if 'type' in request.session and request.session.get('type') != 'member':
        return redirect('login')
    user = request.user
    profile = MemberProfile.objects.get(user=user)
    form = MemberProfileForm(instance=profile)
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('member_profile')
    return render(request, 'member_profile_edit.html', {'form': form})

@login_required
def leader_profile(request):
    if 'type' in request.session and request.session.get('type') != 'leader':
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

@login_required    
def leader_profile_edit(request):
    if 'type' in request.session and request.session.get('type') != 'leader':
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

@login_required
def create_club(request):
    if 'type' in request.session and request.session.get('type') != 'leader':
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

@login_required
def edit_club(request, club_id):
    if 'type' in request.session and request.session.get('type') != 'leader':
        return redirect('leader_login')
    club = get_object_or_404(Club, pk=club_id)
    form = ClubForm(instance=club)
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            club = form.save()
            messages.success(request, 'Club updated successfully')
            return redirect('detail_club', club.id)
    return render(request, 'club_edit.html', {'form': form})
   
@login_required
def remove_club(request, club_id):
    if 'type' in request.session and request.session.get('type') != 'leader':
        return redirect('leader_login')
    club = get_object_or_404(Club, pk=club_id)
    club.delete()
    messages.success(request, 'Club removed successfully')
    return redirect('list_clubs')

def detail_club(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    announcements = Announcement.objects.filter(club=club)
    events = Event.objects.filter(club=club)
    discussions = Discussion.objects.filter(club=club)
    applications = ClubApplication.objects.filter(club=club)
    for a in applications:
        if MemberProfile.objects.filter(user=a.user).exists():        
            a.profile = MemberProfile.objects.get(user=a.user)
        else:
            a.profile = None
    members = club.members.all()
    for member in members:
        if MemberProfile.objects.filter(user=member).exists():
            member.profile = MemberProfile.objects.get(user=member)
        else:
            member.profile = None
    print(f'announcements: {announcements}')
    return render(request, 'club_detail.html', {'club': club, 
                'announcements': announcements, 
                'events': events, 
                'discussions': discussions,
                'applications': applications,
                'members': members
                })

@login_required
def apply_club(request, club_id):
    if 'type' in request.session and request.session.get('type') != 'member':
        return redirect('login')
    user = request.user
    # not a member
    if not user.groups.filter(name='member').exists():
        messages.error(request, 'You are not a member')
        return redirect('list_clubs')
    club = get_object_or_404(Club, pk=club_id)
    if ClubApplication.objects.filter(user=user, club=club).exists():
        messages.error(request, 'You have already applied to this club')
        return redirect('list_clubs')
    application = ClubApplication(user=user, club=club)
    application.save()
    messages.success(request, 'Application sent successfully')
    return redirect('list_clubs')

def leave_club(request, club_id):
    if 'type' in request.session and request.session.get('type') != 'member':
        return redirect('login')
    user = request.user
    club = get_object_or_404(Club, pk=club_id)
    club.members.remove(user)
    # remove user from all events of the club
    try:
        events = Event.objects.filter(club=club)
        for event in events:
            event.members.remove(user)
    except Exception as e:
        print(e)
    # remove user from all discussions of the club
    try:
        discussions = Discussion.objects.filter(club=club)
        for discussion in discussions:
            discussion.members.remove(user)
    except Exception as e:
        print(e)
    # remove user from all topics of the club
    try:
        topics = Topic.objects.filter(discussion__club=club)
        for topic in topics:
            topic.members.remove(user)
    except Exception as e:
        print(e)
    # remove user from all announcements of the club
    try:
        announcements = Announcement.objects.filter(club=club)
        for announcement in announcements:
            announcement.members.remove(user)
    except Exception as e:
        print(e)
    # remove user from all comments of the club
    try:
        comments = Comment.objects.filter(topic__discussion__club=club)
        for comment in comments:
            comment.members.remove(user)
    except Exception as e:
        print(e)    
    messages.success(request, 'You have left the club')
    return redirect('list_clubs')

@login_required
def accept_club(request, caid):
    if 'type' in request.session and request.session.get('type') != 'leader':
        return redirect('leader_login')
    ca = get_object_or_404(ClubApplication, pk=caid)
    club = ca.club
    member = ca.user
    club.members.add(member)
    ca.delete()
    messages.success(request, 'Member accepted successfully')
    return redirect('detail_club', club.id)
    
@login_required
def reject_club(request, caid):
    if 'type' in request.session and request.session.get('type') != 'leader':
        return redirect('leader_login')
    ca = get_object_or_404(ClubApplication, pk=caid)
    club = ca.club
    ca.delete()
    messages.success(request, 'Member rejected successfully')
    return redirect('detail_club', club.id)

@login_required
def remove_member(request, uid, cid):
    if 'type' in request.session and request.session.get('type') != 'leader':
        return redirect('leader_login')
    user = get_object_or_404(User, pk=uid)
    club = get_object_or_404(Club, pk=cid)
    club.members.remove(user)
    # remove user from all events of the club
    try:
        events = Event.objects.filter(club=club)
        for event in events:
            event.members.remove(user)
    except Exception as e:
        print(e)
    # remove user from all discussions of the club
    try:
        discussions = Discussion.objects.filter(club=club)
        for discussion in discussions:
            discussion.members.remove(user)
    except Exception as e:
        print(e)
    # remove user from all topics of the club
    try:
        topics = Topic.objects.filter(discussion__club=club)
        for topic in topics:
            topic.members.remove(user)
    except Exception as e:
        print(e)
    # remove user from all announcements of the club
    try:
        announcements = Announcement.objects.filter(club=club)
        for announcement in announcements:
            announcement.members.remove(user)
    except Exception as e:
        print(e)
    # remove user from all comments of the club
    try:
        comments = Comment.objects.filter(topic__discussion__club=club)
        for comment in comments:
            comment.members.remove(user)
    except Exception as e:
        print(e)    
    messages.success(request, 'Member removed successfully')
    return redirect('detail_club', club.id)

@login_required
def create_event(request, cid):
    if 'type' in request.session and request.session.get('type') != 'leader':
        return redirect('leader_login')
    user = request.user
    club = get_object_or_404(Club, pk=cid)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
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
    if 'type' in request.session and request.session.get('type') != 'leader':
        return redirect('leader_login')
    user = request.user
    event = get_object_or_404(Event, pk=eid)
    club = event.club
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
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
    attendees = event.attendees.all()
    for attendee in attendees:
        if MemberProfile.objects.filter(user=attendee).exists():
            attendee.profile = MemberProfile.objects.get(user=attendee)
        else:
            attendee.profile = None
    return render(request, 'event_detail.html', {'event': event, 'attendees': attendees})

def list_events(request, cid):
    club = get_object_or_404(Club, pk=cid)
    events = Event.objects.filter(club=club)
    return render(request, 'event_list.html', {'events': events, 'club': club})

def remove_event(request, eid):
    if 'type' in request.session and request.session.get('type') != 'leader':
        return redirect('leader_login')
    user = request.user
    event = get_object_or_404(Event, pk=eid)
    event.delete()
    messages.success(request, 'Event removed successfully')
    return redirect('list_events', event.club.id)

def join_event(request,eid):
    if 'type' in request.session and request.session.get('type') != 'member':
        return redirect('login')
    user = request.user
    event = get_object_or_404(Event, pk=eid)
    if event.members.filter(id=user.id).exists():
        messages.error(request, 'You have already joined this event')
        return redirect('list_events', event.club.id)
    event.members.add(user)
    messages.success(request, 'You have joined the event')
    return redirect('detail_event', eid)

def leave_event(request, eid):
    if 'type' in request.session and request.session.get('type') != 'member':
        return redirect('login')
    user = request.user
    event = get_object_or_404(Event, pk=eid)
    event.members.remove(user)
    messages.success(request, 'You have left the event')
    return redirect('list_events', event.club.id)

def create_announcement(request, cid):
    if 'type' in request.session and request.session.get('type') != 'leader':
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
    if 'type' in request.session and request.session.get('type') != 'leader':
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
    club = announcement.club
    likes = LikeAnnouncement.objects.filter(announcement=announcement)
    print(f'likes: {likes} and count: {likes.count()}')
    return render(request, 'ann_detail.html', {'announcement': announcement, 'club': club, 'likes': likes, 'like_count': likes.count()})

def list_announcements(request, cid):
    club = get_object_or_404(Club, pk=cid)
    announcements = Announcement.objects.filter(club=club)
    
    return render(request, 'ann_list.html', {'announcements': announcements, 'club': club})

def delete_announcement(request, aid):
    if 'type' in request.session and request.session.get('type') != 'leader':
        return redirect('leader_login')
    user = request.user
    announcement = get_object_or_404(Announcement, pk=aid)
    announcement.delete()
    messages.success(request, 'Announcement removed successfully')
    return redirect('list_announcements', announcement.club.id)

from .models import LikeAnnouncement
def like_announcement(request, aid):
    if 'type' in request.session and request.session.get('type') != 'member':
        return redirect('login')
    user = request.user
    announcement = get_object_or_404(Announcement, pk=aid)
    if LikeAnnouncement.objects.filter(announcement=announcement, user=user).exists():
        messages.error(request, 'You have already liked this announcement')
        return redirect('detail_announcement', aid)
    like = LikeAnnouncement(announcement=announcement, user=user)
    like.save()
    messages.success(request, 'You have liked the announcement')
    return redirect('detail_announcement', aid)

@login_required
def create_discussion(request, cid):
    user = request.user
    club = get_object_or_404(Club, pk=cid)
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.club = club
            discussion.author = user
            discussion.save()
            messages.success(request, 'Discussion created successfully')
            return redirect('list_discussions', cid)
    else:
        form = DiscussionForm()
    return render(request, 'dis_create.html', {'form': form, 'club': club})

@login_required
def edit_discussion(request, did):
    # if discussion is created by current user
    discussion = get_object_or_404(Discussion, pk=did)
    if discussion.author != request.user:
        messages.error(request, 'You are not allowed to edit this discussion')
        return redirect('list_discussions', discussion.club.id)
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

@login_required
def detail_discussion(request, did):
    discussion = get_object_or_404(Discussion, pk=did)
    topics = Topic.objects.filter(discussion=discussion)
    for topic in topics:
        topic.comment_count = Comment.objects.filter(topic=topic).count()
    return render(request, 'dis_detail.html', {'discussion': discussion, 'topics': topics})


@login_required
def list_discussions(request, cid):
    club = get_object_or_404(Club, pk=cid)
    discussions = Discussion.objects.filter(club=club)
    topics = Topic.objects.filter(discussion__club=club)
    for topic in topics:
        topic.comment_count = Comment.objects.filter(topic=topic).count()
    return render(request, 'dis_list.html', {'discussions': discussions, 'club': club, 'topics': topics})

def remove_discussion(request):
    if 'type' in request.session and request.session.get('type') != 'leader':
        return redirect('leader_login')
    user = request.user
    discussion_id = request.GET['discussion_id']
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    discussion.delete()
    messages.success(request, 'Discussion removed successfully')
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
    user = request.user
    discussion = get_object_or_404(Discussion, pk=did)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.discussion = discussion
            topic.author = user
            topic.save()
            messages.success(request, 'Topic created successfully')
            return redirect('list_topics', did)
    else:
        form = TopicForm()
    return render(request, 'topic_create.html', {'form': form, 'discussion': discussion})


def edit_topic(request, tid):
    user = request.user
    topic = get_object_or_404(Topic, pk=tid)
    discussion = topic.discussion
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
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
    form = CommentForm()
    
    return render(request, 'topic_detail.html', {
        'topic': topic, 
        'form': form,
        'comments': comments})

def list_topics(request, did):
    discussion = get_object_or_404(Discussion, pk=did)
    topics = Topic.objects.filter(discussion=discussion)
    return render(request, 'topic_list.html', {'topics': topics, 'discussion': discussion})

def remove_topic(request, tid):
    user = request.user
    topic = get_object_or_404(Topic, pk=tid)
    if topic.author != user:
        messages.error(request, 'You are not allowed to delete this topic')
        return redirect('list_topics', topic.discussion.id)
    topic.delete()
    messages.success(request, 'Topic removed successfully')
    return redirect('list_topics', topic.discussion.id)

def create_comment(request, tid):
    user = request.user
    topic = get_object_or_404(Topic, pk=tid)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.author = user
            comment.save()
            messages.success(request, 'Comment created successfully')
    return redirect('detail_topic', tid)

def edit_comment(request, cid):
   
    user = request.user
    comment = get_object_or_404(Comment, pk=cid)
    topic = comment.topic
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.author = user
            comment.save()
            messages.success(request, 'Comment updated successfully')
    return redirect('detail_topic', topic.id)

def remove_comment(request, cid):
    user = request.user
    comment = get_object_or_404(Comment, pk=cid)
    if comment.author != user:
        messages.error(request, 'You are not allowed to delete this comment')
        return redirect('detail_topic', comment.topic.id)
    comment.delete()
    messages.success(request, 'Comment removed successfully')
    return redirect('detail_topic', comment.topic.id)
        
def home(request):
    clubs = Club.objects.all()
    return render(request, 'index.html', {'clubs': clubs})



