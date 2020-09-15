# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

vaildPaths = ['/index/','/createTask/','/config/','/run/','/modify/']

class URLMiddleware(MiddlewareMixin):
    # handle HTTP request
    def process_request(self, request):
        if request.path == '/index/':
            print("request.POST.get('username')=" + str(request.POST.get('username')))
            # it seems like used to logined.
            if request.session.has_key('username'):
                # not logined, must login first
                if request.session['username'] == None:
                    return render(request, 'login.html')
                # logined
                elif request.session['username'] != None :
                    print(request.session['username'])
                    pass;
            #if never/not logined
            else: #not request.session.has_key('username'):
                # login request
                if request.POST.get('username') != None:
                    pass;
                # any others shuold login firstly
                else:
                    return render(request, 'login.html');

        elif request.session.get('username', None):
                pass
        else:
            return render(request, 'login.html')

    # handle HTTP response
    def process_response(self, request, response):
        return response