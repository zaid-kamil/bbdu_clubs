from django.contrib import admin
from .models import Club, Event, Announcement, Discussion, Topic, Comment, LeaderProfile, MemberProfile, Faq, Contact, ClubApplication
from .models import LikeAnnouncement
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(Announcement)
admin.site.register(Discussion)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(LeaderProfile)
admin.site.register(MemberProfile)
admin.site.register(Faq)
admin.site.register(Contact)
admin.site.register(ClubApplication)
admin.site.register(LikeAnnouncement)