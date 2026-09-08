from django.urls import path
from portofolio_main.views import show_main, show_experience

app_name = "portofolio_main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
]