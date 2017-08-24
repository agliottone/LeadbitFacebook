from django.shortcuts import render
from .models import Lead, Request, Campagna
import feedparser
import requests


#carica su x il pannello
def cron3(request):
    salvati=[]
    falliti=[]
    errori=[]
    leads = Lead.objects.filter(elaborato=False,campagna__tipologia=2).all()
    for lead in leads:
      try:
        requestobj = Request(api=lead.campagna.api,raw=lead.postdata,lead=lead)
        response = requests.post(requestobj.api, data=requestobj.raw)
        requestobj.response = response.content
        if requestobj.response == '{"status":"success"}':
          requestobj.successo=True
          lead.elaborato = True
        else:
          requestobj.successo=False
        requestobj.save()
      except Exception, e:
        #falliti.append(lead)
        errori.append(str(requestobj.raw) +": " + str(e))
      else:
          lead.save()
          salvati.append(requestobj)
          
    return render(request, 'cron2.html', {"leads":leads,"salvati":salvati,"falliti": [],"errori":[]})
  
  
  
#carica su i lead leadbit
def cron2(request):
    salvati=[]
    falliti=[]
    errori=[]
    leads = Lead.objects.filter(elaborato=False,campagna__tipologia=1).all()
    for lead in leads:
      try:
        requestobj = Request(api=lead.campagna.api,raw=lead.postdata,lead=lead)
        response = requests.post(requestobj.api, data=requestobj.raw)
        requestobj.response = response.content
        if requestobj.response == '{"status":"success"}':
          requestobj.successo=True
        else:
          requestobj.successo=False
        requestobj.save()
      except Exception, e:
        #falliti.append(lead)
        errori.append(str(requestobj.raw) +": " + str(e))
      else:
          lead.elaborato = True
          lead.save()
          salvati.append(requestobj)
          
    return render(request, 'cron2.html', {"leads":leads,"salvati":salvati,"falliti": [],"errori":[]})
  
#scarica i lead nel db
def cron(request):
    salvati=[]
    falliti=[]
    errori=[]
    campagne = Campagna.objects.all()
    for campagna in campagne:
      feed = feedparser.parse(campagna.rss)

      for post in feed.entries:
        post.fbad=post.title
        post.fbid=post.link.split("/")[-1:][0]
        desc = post.description
        pezzi = desc.split("|")
        post.fbdate=pezzi[0]
        post.name=pezzi[1]
        post.phone=pezzi[2]
        post.obj = Lead(campagna=campagna)
        post.obj.phone=post.phone
        post.obj.name=post.name
        post.obj.fbid=post.fbid
        post.obj.fbad=post.fbad
        post.obj.fbdate=post.fbdate
        post.obj.elaborato=False
        
        try:
          post.obj.save()
        except Exception, e:
          falliti.append(post)
          errori.append(post.name + " - " + post.fbad +": " + str(e))
        else:
          salvati.append(post)
    return render(request, 'cron.html', {"feed":feed.entries, "campagne":campagne,"salvati":salvati,"falliti":[],"errori":[]})
  
# Create your views here.
