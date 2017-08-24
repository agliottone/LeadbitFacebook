from django.core.urlresolvers import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import *
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields
import datetime

TIPOLOGIA =(
   ( 1, 'LEADBIT'),
    (2 , 'PANNELLO'),
)


class Campagna(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    rss = models.CharField(max_length=255,blank=True)
    api = models.CharField(max_length=255,blank=True)
    flow_hash = models.CharField(max_length=255,blank=True)
    landing = models.CharField(max_length=255,blank=True)
    country = models.CharField(max_length=255,default="IT")  
    prodotto = models.IntegerField(blank=True,null=True)
    qta = models.IntegerField(blank=True,null=True)
    tipologia = models.IntegerField(max_length=255,blank=True, choices=TIPOLOGIA,default=1)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural="campagne"

    def __unicode__(self):
        return u'%s %s' % (self.pk,self.name)

class Lead(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    phone = models.CharField(max_length=255)
    fbad = models.CharField(max_length=255)
    fbid = models.CharField(max_length=255,unique=True)
    fbdate = models.CharField(max_length=255)
    elaborato = models.BooleanField(default=False)
    campagna = models.ForeignKey('Campagna',related_name="leads" )
    
    @property
    def postdata(self):
      if(self.campagna.tipologia==1):
        postdata= {'name':self.name,'phone':self.phone.replace(" ",""), 'country':self.campagna.country,'flow_hash':self.campagna.flow_hash}
        postdata['landing']=self.campagna.landing
        postdata['referrer']=self.campagna.landing
        postdata['sub1']=postdata['name']
        postdata['sub2']=postdata['phone']
        postdata['sub3']=postdata['landing']
        postdata['sub4']=datetime.datetime.now().strftime('%d/%m%Y %H:%M:%S')
        return postdata
      else: #caso pannello
        nome= self.name
        cognome=""
        try:
          nome = nome.split(" ")[0]
          cognome =" ".join( self.name.split(" ")[1:])
        except:
          pass
        postdata= {'nome':nome,'telefono':self.phone.replace(" ",""), 'country':self.campagna.country}
        postdata['cognome']=cognome
        postdata['fbad']=self.fbad
        postdata['fbid']=self.fbid
        postdata['qta']=self.campagna.qta
        postdata['prodotto']=self.campagna.prodotto
        return postdata
      
    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s %s' % (self.pk,self.name)


class Request(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    raw = models.TextField(max_length=1000)
    api = models.CharField(max_length=255,blank=True)
    response = models.TextField(max_length=100)
    successo = models.BooleanField()

    # Relationship Fields
    lead = models.ForeignKey('Lead', related_name='requests')

  
    class Meta:
        ordering = ('-created',)
        verbose_name_plural="Richieste"

    def __unicode__(self):
        return u'%s' % self.pk