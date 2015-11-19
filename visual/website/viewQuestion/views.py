#coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from models import Question
# from models import Image
from bs4 import BeautifulSoup

def addImage(text):
        soup = BeautifulSoup(text)
        imgs = soup.find_all("img")
        for img in imgs:
                if img["src"][0:7] != "http://":
                        img["src"] = "/static/image/" + img["src"] + ".jpg"
        return str(soup) 

def view(request, limit, offset, subject, qtype):
        limit = int(limit)
        offset = int(offset)
        subject = int(subject)
        qtype = int(qtype)
        questionList = []
        if subject == -1 and qtype == -1:
                questionList = Question.objects.all()[offset: offset + limit]
        elif qtype == -1:
                questionList = Question.objects.all().filter(subject=subject)[offset: offset + limit]
        else:
                questionList = Question.objects.all().filter(subject=None).filter(type=qtype)[offset: offset + limit]
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
        #                         i["src"] = "/images/images/" + i["src"]
        #         text += str(soup) 
        # return HttpResponse(text)


def deleteQuestion(request, id):
        questions = Question.objects.filter(id=id)
        for q in questions:
                q.delete()
        return HttpResponse("Success")
'''
def getImage(request, id):
        text = ""
        #text = id
        img = Image.objects.filter(id=id)
        if len(img) != 0:
                text = img[0].data
        return HttpResponse(text)

'''

def main(request):
        return render_to_response('center.html', locals())

# Create your views here.
