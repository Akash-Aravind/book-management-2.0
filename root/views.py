from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView
from django.shortcuts import render
from .models import Wishlist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import requests
# Create your views here.


@login_required
def wishlist(request, isbn, title):
    try:
        Wishlist.objects.get(
            name=request.user, product=isbn)
        return render(request, 'beginner.html', {
            'success': f'Hey {request.user} {title} has already been added',
        })
    except:
        fetchurl = f"https://www.googleapis.com/books/v1/volumes?q={title}&key=AIzaSyAJ8nHtE3NlGpfnhN1jTT_0FvC49dyf1bo"
        data = requests.get(fetchurl)
        binfo = data.json()
        imgvar = binfo['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        context = Wishlist.objects.create(
            name=request.user, product=isbn, imageurl=imgvar, title=title)
        return redirect('http://localhost:8000/wishlist')


def SearchPage(request):
    searchtext = request.POST.get("searchtext")

    fetchurl = f"https://www.googleapis.com/books/v1/volumes?q={searchtext}&maxResults=40&key=AIzaSyAJ8nHtE3NlGpfnhN1jTT_0FvC49dyf1bo"
    data = requests.get(fetchurl)
    res = data.json()

    return render(request, 'search.html', {
        'queryresults': res["items"],
    })


@login_required
def removewishlist(request, isbnum):
    rem = Wishlist.objects.get(product=isbnum, name=request.user.username)
    rem.delete()
    return redirect('http://localhost:8000/wishlist')


class WishListView(LoginRequiredMixin, TemplateView):
    template_name = "wishview.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["dat"] = Wishlist.objects.all().filter(
            name=self.request.user.username)
        return context


class DetailPage(TemplateView):
    template_name = "detail.html"

    def get(self, request, title):
        fetchurl = f"https://www.googleapis.com/books/v1/volumes?q={title}&key=AIzaSyAJ8nHtE3NlGpfnhN1jTT_0FvC49dyf1bo"
        data = requests.get(fetchurl)
        binfo = data.json()
        return render(request, 'detail.html', {
            'bookinfo': binfo["items"][0],
        })


class HomePage(TemplateView):
    def get(self, request):
        name = request.user
        data = requests.get(
            "https://api.nytimes.com/svc/books/v3/lists/overview.json?api-key=4eqGqpcgPr09d47XDHGaU7UU2sX7ZFxo")
        beta = data.json()

        template_name = "index.html"
        return render(request, 'index.html', {
            'ip': beta["results"]["lists"],
            'nam': name,
        })
