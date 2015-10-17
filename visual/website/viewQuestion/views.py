#coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render
from models import Question
from models import Image
from bs4 import BeautifulSoup

def index(request, limit, offset):
        text = ""
        limit = int(limit)
        offset = int(offset)
        for i in Question.objects.all()[offset: offset + limit]:
                soup = BeautifulSoup(i.content)
                imgs = soup.find_all("img")
                for i in imgs:
                        if i["src"][0:7] != "http://":
                                i["src"] = "/image/" + i["src"]
                text += str(soup) 
        return HttpResponse(text)

def getImage(request, id):
        text = ""
        #text = id
        img = Image.objects.filter(id=id)
        if len(img) != 0:
                text = img[0].data
        return HttpResponse(text)

# Create your views here.
