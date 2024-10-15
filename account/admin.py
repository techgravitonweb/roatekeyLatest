from django.contrib import admin
from .models import *
from adsapi.models import AdminAuth
# Register your models here.
from .models import PhoneOTP
admin.site.register(PhoneOTP)
admin.site.register(User)
admin.site.register(AdminAuth)
admin.site.register(ReviewSection)
admin.site.register(TelemetryDaa)
admin.site.register(JobApply)
admin.site.register(JobsRequired)   
