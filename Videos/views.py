from django.shortcuts import render, redirect
from .forms import VideoForm

def upload(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = VideoForm()
    return render(request,'upload.html',{'form':form})