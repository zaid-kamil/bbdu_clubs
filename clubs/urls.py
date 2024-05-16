from django.urls import path
from .import views


urlpatterns = [
    # auth
    path("login", views.member_login, name="login"),
    path("register", views.member_register, name="register"),
    
    # leader auth
    path("leader/login", views.leader_login, name="leader_login"),
    path("leader/register", views.leader_register, name="leader_register"),
    
    # logout
    path('logout', views.logout_view, name='logout'),
    # member profiles
    path('member/profile', views.member_profile, name='member_profile'),
    path('member/profile/edit', views.member_profile_edit, name='member_profile_edit'),
    
    # leader profile
    path('leader/profile', views.leader_profile, name='leader_profile'),
    path('leader/profile/edit', views.leader_profile_edit, name='leader_profile_edit'),
    
    # club urls 
    path('club/list', views.list_clubs, name='list_clubs'),
    path('club/search', views.search_club, name='search_club'),
    path('club/create', views.create_club, name='create_club'),
    path('club/edit/<int:club_id>/', views.edit_club, name='edit_club'),
    path('club/remove/<int:club_id>/', views.remove_club, name='remove_club'),
    path('club/detail/<int:club_id>/', views.detail_club, name='detail_club'),
    path('club/apply/<int:club_id>/', views.apply_club, name='apply_club'),
    path('club/leave/<int:club_id>/', views.leave_club, name='leave_club'),
    path('club/accept/<int:caid>/', views.accept_club, name='accept_in_club'),
    path('club/reject/<int:caid>/', views.reject_club, name='reject_in_club'),
    path('club/remove/<int:uid>/<int:cid>/', views.remove_member, name='remove_member'),
    
    # event urls
    path('event/list/<int:cid>/', views.list_events, name='list_events'),
    path('event/detail/<int:eid>/', views.detail_event, name='detail_event'),
    path('event/create/<int:cid>/', views.create_event, name='create_event'),
    path('event/edit/<int:eid>/', views.edit_event, name='edit_event'),
    path('event/remove/<int:eid>/', views.remove_event, name='remove_event'),
    path('event/join/<int:eid>/', views.join_event, name='join_event'),
    path('event/leave/<int:eid>/', views.leave_event, name='leave_event'),
    
    # announcement urls
    path('announce/create/<int:cid>/', views.create_announcement, name='create_announcement'),
    path('announce/edit/<int:aid>/', views.edit_announcement, name='edit_announcement'),
    path('announce/detail/<int:aid>/', views.detail_announcement, name='detail_announcement'),
    path('announce/list/<int:cid>/', views.list_announcements, name='list_announcements'),
    path('announce/delete/<int:aid>/', views.delete_announcement, name='remove_announcement'),
    path('announce/like/<int:aid>/', views.like_announcement, name='like_announcement'),
    
    # discussion urls
    path('dis/list/<int:cid>/', views.list_discussions, name='list_discussions'),
    path('dis/create/<int:cid>/', views.create_discussion, name='create_discussion'),
    path('dis/edit/<int:did>/', views.edit_discussion, name='edit_discussion'),
    path('dis/detail/<int:did>/', views.detail_discussion, name='detail_discussion'),
    path('dis/remove/<int:did>/', views.remove_discussion, name='remove_discussion'),
    
    # topic urls
    path('topic/create/<int:did>/', views.create_topic, name='create_topic'),
    path('topic/edit/<int:tid>/', views.edit_topic, name='edit_topic'),
    path('topic/detail/<int:tid>/', views.detail_topic, name='detail_topic'),
    path('topic/list/<int:did>/', views.list_topics, name='list_topics'),
    path('topic/remove/<int:tid>/', views.remove_topic, name='remove_topic'),
    
    # comment urls
    path('comment/create/<int:tid>/', views.create_comment, name='create_comment'),
    path('comment/edit/<int:cid>/', views.edit_comment, name='edit_comment'),
    path('comment/remove/<int:cid>/', views.remove_comment, name='remove_comment'),
    
    # communications
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    
    # home
    path('', views.home, name='home'),
]
