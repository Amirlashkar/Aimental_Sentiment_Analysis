from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .Analyser import analyser
from .models import User


def login(request):
    render_dict = {}
    if request.method == "POST":
        if "login" in request.POST:
            request.session["username"] = request.POST["username"]
            request.session["password"] = request.POST["password"]
            render_dict["username"] = request.session["username"]
            render_dict["password"] = request.session["password"]
            if not User.objects.filter(name=request.session["username"], password=request.session["password"]).exists():
                user = User(name=request.session["username"], password=request.session["password"])
                user.save()
            else:
                user = User.objects.get(name=request.session["username"], password=request.session["password"])

            return redirect("/sentiment_analyser/analyser")

    return render(request, "login.html", render_dict)


def sent_anal(request):     
    if not User.objects.filter(name=request.session["username"], password=request.session["password"]).exists():
        user = User(name=request.session["username"], password=request.session["password"])
        user.save()
    else:
        user = User.objects.get(name=request.session["username"], password=request.session["password"])

    if not user.time_set.all().exists():
        time = user.time_set.create(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    elif (datetime.now() - datetime.strptime(user.time_set.last().time, "%Y-%m-%d %H:%M:%S")).total_seconds() > 300:
        time = user.time_set.create(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        time = user.time_set.last()

    render_dict = {"models": {"emoji": "Emoji", "emotion": "Emotion",
     "hate": "Hatefulness", "irony": "Ironicaly", "offensive": "Offensive", "sentiment": "Sentiment"}}

    if request.method == "POST":
        if "confirm" in request.POST:
            if "model" not in request.POST and "model_t" not in list(request.session.keys()):
                messages.error(request, "Please Select an Aspect!")
                return redirect("/sentiment_analyser/analyser")

            elif "text" not in request.POST and "text" not in list(request.session.keys()):
                messages.error(request, "Please Enter any text")
                return redirect("/sentiment_analyser/analyser")
            
            elif "model" in request.POST and "model_t" in list(request.session.keys()):
                request.session["text"] = request.POST["text"]
                request.session["model_t"] = request.POST["model"]

            elif "model" not in request.POST and "model_t" in list(request.session.keys()):
                if request.POST["text"] != request.session["text"]:
                    request.session["text"] = request.POST["text"]

                elif request.POST["model"] != request.session["model_t"]:
                    request.session["model_t"] = request.POST["model"]
                

            request.session["analysis"] = analyser(request.session["text"], request.session["model_t"])
            
            render_dict["text"] = request.session["text"]
            render_dict["model_t"] = request.session["model_t"]
            render_dict["analysis"] = request.session["analysis"]

    print(request.POST)
    print(render_dict)
    for key, val in request.session.items():
        print(key, val)

    re = time.render_set.create(rd=render_dict)
    re.save()
    return render(request, "sent_anal.html", render_dict)