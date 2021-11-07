from django.shortcuts import render
import requests

def startPage(request):
	return render(request, 'generateClassifier.html')
	