#coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from models import Question
# from models import Image
from bs4 import BeautifulSoup

import json
import csv

def addImage(text, desc):
        soup = BeautifulSoup(text)
        imgs = soup.find_all("img")
        descList = desc.split(">")
        img_dir = "/static/images"
        for item in descList:
            img_dir += "/" + item.strip()
        for img in imgs:
                if img["src"][0:7] != "http://":
                        img["src"] = img_dir + "/" + img["src"]
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
                i.content = addImage(i.content,i.description)
                i.rightanswer = addImage(i.rightanswer,i.description)
                i.answerexplain = addImage(i.answerexplain,i.description)
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
                return u"英语"
        if num == 1:
                return u"数学"
        return u"其他"         
        
def parseType(num):
        if num == 0:
                return u"单选题"
        if num == 1:
                return u"多选题"       
        if num == 2:
                return u"解答题"
        if num == 5:
                return u"完形填空"
        return u"其他"

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
        qcsvfile.write(u'\ufeff'.encode('utf-8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        # qwriter = csv.writer(qcsvfile)
        #iwriter = csv.writer(icsvfile)
        try:
            headers = [u'学科', u'题型', u'id', u'具体分类', u'HTML内容', u'HTML正确答案', u'HTML解释', u'难度', u'正确率', u'热度', 'A', 'B', 'C', 'D', u'来源', u'纯文本']
            for i in range(len(headers)):
                headers[i] = headers[i].encode('utf-8')
            qwriter = csv.DictWriter(qcsvfile, headers)
            qwriter.writeheader()
            # qwriter.writerow(headers)    
            #iwriter,writerow(['id', 'url'])
            for i in questionList:
                row = [parseSubject(i.subject), parseType(i.type), i.id, i.description, i.content, i.rightanswer, i.answerexplain, i.difficulty, i.rightrate, i.hot, i.A, i.B, i.C, i.D, i.source, i.plainText]
                # for i in range(len(row)):
                    # row[i] = unicode(row[i]).encode("utf-8")
                qwriter.writerow( {headers[i]: unicode(row[i]).encode("utf-8")  for i in range(len(row))} )
        # print i.difficulty
        except Exception, e:
            print e
        qcsvfile.close() 
        return HttpResponse(json.dumps({'status': 'success'}))
            

def main(request):
        return render_to_response('center.html', locals())

# Create your views here.
