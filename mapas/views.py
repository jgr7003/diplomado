# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    # return HttpResponse("You're looking at question %s.")
    return render(request, 'mapas/index.html')