from django.contrib import admin
from django import forms
from .models import Lead, Request, Campagna

class LeadAdminForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = '__all__'


class LeadAdmin(admin.ModelAdmin):
    form = LeadAdminForm
    list_filter = ('campagna',) 
    list_display = ['name','campagna', 'phone', 'fbad', 'fbid', 'fbdate', 'elaborato','created', 'last_updated']
    list_editable=('elaborato',)
    
admin.site.register(Lead, LeadAdmin)


class RequestAdminForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = '__all__'


class RequestAdmin(admin.ModelAdmin):
    form = RequestAdminForm
    list_display = [ 'lead','raw', 'response', 'successo','created', 'last_updated']

admin.site.register(Request, RequestAdmin)


class CampagnaAdminForm(forms.ModelForm):

    class Meta:
        model = Campagna
        fields = '__all__'


class CampagnaAdmin(admin.ModelAdmin):
    form = CampagnaAdminForm
    list_display = ['name', 'rss', 'api','flow_hash','country','landing','created', 'last_updated' ,'qta','prodotto','tipologia']

admin.site.register(Campagna, CampagnaAdmin)
