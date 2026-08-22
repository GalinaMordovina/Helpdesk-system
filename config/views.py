from django.shortcuts import render


def home(request):
    """Отображает главную страницу веб-интерфейса."""

    return render(request, "home.html")
