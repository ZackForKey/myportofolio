from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2506657011', 
        'name': 'Mohammad Zaky Prastio',  
        'class': 'PBP B',     }

    return render(request, "main.html", context)
