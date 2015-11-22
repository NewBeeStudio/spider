#coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from models import Question
# from models import Image
from bs4 import BeautifulSoup

import json
import csv

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
        elif subject == -1:
                questionList = Question.objects.all().filter(type=qtype)[offset: offset + limit]
        else:
                questionList = Question.objects.all().filter(subject=subject).filter(type=qtype)[offset: offset + limit]
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

def parseSubject(num):
        if num == 0:
                return "英语"
        if num == 1:
                return "数学"
        return "其他"         
        
def parseType(num):
        if num == 0:
                return "单选题"
        if num == 1:
                return "多选题"       
        if num == 2:
                return "解答题"
        if num == 5:
                return "完形填空"
        return "其他"

def excel(request, limit, offset, subject, qtype):
        limit = int(limit)
        offset = int(offset)
        subject = int(subject)
        qtype = int(qtype)
        questionList = []
        if (limit != -1):
                if subject == -1 and qtype == -1:
                        questionList = Question.objects.all()[offset: offset + limit]
                elif qtype == -1:
                        questionList = Question.objects.all().filter(subject=subject)[offset: offset + limit]
                elif subject == -1:
                        questionList = Question.objects.all().filter(type=qtype)[offset: offset + limit]
                else:
                        questionList = Question.objects.all().filter(subject=subject).filter(type=qtype)[offset: offset + limit]
        else:
                if subject == -1 and qtype == -1:
                        questionList = Question.objects.all()
                elif qtype == -1:
                        questionList = Question.objects.all().filter(subject=subject)
                elif subject == -1:
                        questionList = Question.objects.all().filter(type=qtype)
                else:
                        questionList = Question.objects.all().filter(subject=subject).filter(type=qtype) 
        qcsvfile = file('question.csv', 'wb')
        #icsvfile = file('image.csv', 'wb')
        qwriter = csv.writer(qcsvfile)
        #iwriter = csv.writer(icsvfile)
        qwriter.writerow(['学科', '题型', 'id', '具体分类', 'HTML内容', 'HTML正确答案', 'HTML解释', '难度', '正确率', '热度', 'A', 'B', 'C', 'D', '来源', '纯文本'])    
        #iwriter,writerow(['id', 'url'])
        for i in questionList:
                qwriter.writerow([parseSubject(i.subject), parseType(i.type), i.id, i.description, i.content, i.rightanswer, i.answerexplain, i.difficulty, i.rightrate, i.hot, i.A, i.B, i.C, i.D, i.source, i.plainText]) 
        qcsvfile.close() 
        return HttpResponse(json.dumps({'status': 'success'}))
            

def main(request):
        return render_to_response('center.html', locals())

# Create your views here.
