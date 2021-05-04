from django.shortcuts import render

# Create your views here.
def graphs(request):
    context = {}
    return render(request, 'graphs.html', context)

