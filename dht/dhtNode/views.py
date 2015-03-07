#coding:utf-8
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django import forms
from dht.dhtNode.documents import dht_node
from djangosolr.documents import Q
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def home(request):
    return render_to_response('index.html',{'title': 'title哈哈'},context_instance=RequestContext(request))#第二个参数为自定义变量

class CharacterForm(forms.Form):
    searchinput = forms.CharField(max_length = 1024)
ONE_PAGE_OF_DATA = 8
def search(request):

    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage','1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    #判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA

    if request.GET:
        form = CharacterForm(request.GET)
        if form.is_valid():
            searchinput = form.cleaned_data['searchinput']
            if searchinput != None and searchinput != '':
                try:
                    if searchinput != 'name':
                        dhts = dht_node.documents.q(Q(name=searchinput) | Q(files=searchinput))[startPos:endPos]
                    else:
                        dhts = dht_node.documents.q(Q(files=searchinput))[startPos:endPos]

                    if curPage == 1 and allPage == 1: #标记1
                        allPostCounts = dhts.count()
                        allPage = allPostCounts / ONE_PAGE_OF_DATA
                        remainPost = allPostCounts % ONE_PAGE_OF_DATA
                    if remainPost > 0:
                        allPage += 1
                    for dht in dhts:

                        #处理高亮
                        name = dht.name
                        name = name.replace(searchinput,"<font style='color:red'>" + searchinput + "</font>")
                        dht.name = name
                        files = []
                        file_count = 0
                        file_max_size = 0
                        for k in eval(dht.file_list):
                            title = k[0]
                            unit = 'b'
                            size = k[1]
                            if size >= 1024:
                                unit = 'K'
                                size = size/1024
                            if size >= 1024:
                                unit = 'M'
                                size = size/1024
                            if size >= 1024:
                                unit = 'G'
                                size = size/1024
                            file_info = str(k[0]) + "  " + str(size) + unit
                            files.append(file_info)
                            file_count += 1
                            if file_max_size <= k[1]:
                                file_max_size = k[1]
                                dht.file_max_size = str(size) + unit
                        dht.file_query_list = files[:3]
                        dht.file_count = file_count
                except Exception,e:
                    print e
    #计算要显示的页码列表
    showPageNums = []

    if curPage >= 3 and allPage >= (curPage+3):
        for i in range(curPage-3,curPage+3):
            showPageNums.append(i+1)
    elif curPage >=3 and allPage < (curPage+3):
        for i in range(curPage-3,allPage):
            showPageNums.append(i+1)
    elif curPage < 3 and allPage >= (curPage+3):
        for i in range(0,curPage+3):
            showPageNums.append(i+1)
    elif curPage < 3 and allPage < (curPage+3):
        for i in range(0,allPage):
            showPageNums.append(i+1)
    return render_to_response('search_result_list.html',{'result': dhts,'searchinput':searchinput,'allPage':allPage, 'curPage':curPage,'showPageNums':showPageNums},context_instance=RequestContext(request))

def search_detail(request):
    hashinfo = request.GET.get('hashinfo')
    searchinput = request.GET.get('searchinput')

    dhts = dht_node.documents.q(Q(hashInfo=hashinfo))

    dht = dhts[0]

    files = []
    file_count = 0
    file_max_size = 0
    for k in eval(dht.file_list):
        title = k[0]
        unit = 'b'
        size = k[1]
        if size >= 1024:
            unit = 'K'
            size = size/1024
        if size >= 1024:
            unit = 'M'
            size = size/1024
        if size >= 1024:
            unit = 'G'
            size = size/1024
        file_info = str(k[0]) + "  " + str(size) + unit
        files.append(file_info)
        file_count += 1
        if file_max_size <= k[1]:
            file_max_size = k[1]
            dht.file_max_size = str(size) + unit
    dht.file_query_list = files
    dht.file_count = file_count
    return render_to_response('search_result_detail.html',{'dht_detail': dht,'searchinput':searchinput},context_instance=RequestContext(request))
