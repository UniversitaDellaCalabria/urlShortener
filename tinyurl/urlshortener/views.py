from django.shortcuts import render

def urlshortener(request):
    context = dict(
        project_name='Url Shortener'
    )
    return render(request, 'urlshortener.html', context)
