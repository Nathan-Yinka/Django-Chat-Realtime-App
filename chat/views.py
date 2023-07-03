from django.shortcuts import render, redirect ,HttpResponse
from chat.models import Room, Message
from django.http import JsonResponse
import json

# Create your views here.

def index(request):
    return render(request, "index.html")

def room(request,room):
    username = request.GET.get("username")
    if Room.objects.filter(name = room).exists():
        print(room)
        room_detail = Room.objects.get(name = room)
        return render(request, "room.html",{
            "username": username,
            "room_detail":room_detail,
            "room" : room
    })
    return render(request, "room.html")

def checkview(request):
    if request.method == 'POST':
        room = request.POST["room_name"]
        username = request.POST["username"]
        
        if Room.objects.filter(name = room).exists():
            return redirect(f"{room}/?username={username}")
        else:
            new_room = Room.objects.create(name = room)
            new_room.save()
            return redirect(f"{room}/?username={username}")
    else:
        return render(request, "index.html")
    
        
def send(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            # Now 'data' contains the normal Python data from the JSON string
            username = data.get('username')
            room_id = data.get('room_id')
            message = data.get('message')
            new_message = Message.objects.create(value= message, user=username, room= room_id)
            new_message.save()
    return  HttpResponse("message sent")

def getMessages(request,room):
    room_detail = Room.objects.get(name=room)
    message = Message.objects.filter(room=room_detail.id)
    return JsonResponse({"messages":list(message.values())})
    