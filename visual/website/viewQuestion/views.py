#coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from models import Question
from models import Image
from bs4 import BeautifulSoup

def addImage(text):
        soup = BeautifulSoup(text)
        imgs = soup.find_all("img")
        for img in imgs:
                if img["src"][0:7] != "http://":
                        img["src"] = "/static/images/" + img["src"] + ".jpg"
        return str(soup)

def view(request, limit, offset):
        limit = int(limit)
        offset = int(offset)
        questionList = Question.objects.all()[offset: offset + limit]
        subjects = {"0": u"数学", "1":u"语文", "2":u"英语","3": u"物理", "4":u"化学", "5":u"生物", "6":u"历史", "7":u"地理", "8":u"政治"}
        for i in questionList:
                i.content = addImage(i.content)
                i.rightanswer = addImage(i.rightanswer)
                i.answerexplain = addImage(i.answerexplain)
        return render_to_response('questions.html', locals())
        # text = ""
        # for i in Question.objects.all()[offset: offset + limit]:
        #         soup = BeautifulSoup(i.content)
        #         imgs = soup.find_all("img")
        #         for i in imgs:
        #                 if i["src"][0:7] != "http://":
        #                         i["src"] = "/image/" + i["src"]
        #         text += str(soup) 
        # return HttpResponse(text)

def getImage(request, id):
        text = ""
        #text = id
        img = Image.objects.filter(id=id)
        if len(img) != 0:
                text = img[0].data
        return HttpResponse(text)

def main(request):
        return render_to_response('center.html', locals())

# Create your views here.
