from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.db.models import Max
from django.db.models import Sum
from .models import BowlingGame
from api.serializers import BowlingGameSerializer
import datetime
import random

# Create your views here.


def start_game(request):
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max'] + 1 #Get ID for the game
    BowlingGame.objects.bulk_create(eval(open("game/constants/bulk_list.txt").read())) #Create the game frame. eval is just space saver
    global button_name
    button_name = 'mycalc'
    return HttpResponseRedirect('/play/') #Redirect to the play rout. This method allows path only as argument


button_name = 'mycalc'
def initial_load(request): #This func is doing the frontend while the game is running except end page
    # vars needed for the render
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    game_frame = BowlingGame.objects.filter(GameId=a)
    total = BowlingGame.objects.filter(GameId=a).aggregate(Sum('Result'))['Result__sum']
    exit = BowlingGame.objects.filter(GameId=a).aggregate(Max('StateOfGame'))['StateOfGame__max']

    d, m = {}, 1 #This is just to save few lines. It's good in combination with 'eval' but at the end I have just dict instead of query which is bad
    for x in range(1, 11):
        d["result_frame_{0}".format(x)] = BowlingGame.objects.filter(GameId=a, Frame=m).aggregate(Sum('Result'))['Result__sum']
        m += 1


    if button_name == 'mycalc':
        return render(request, 'play.html', eval(open("game/constants/render_dict_play.txt").read()))
    elif button_name == 'mybow':
        #if exit == 1: #Check the status of the game and exit it when is 2. Consider bool
            #global button_name
            #button_name = 'mycalc'
        game_frame = serializers.serialize('json', game_frame)
        return JsonResponse({'total': total, 'game_frame': game_frame, 'result_frame_1': d['result_frame_1'],
                             'result_frame_2': d['result_frame_2'], 'result_frame_3': d['result_frame_3'],
                             'result_frame_4': d['result_frame_4'], 'result_frame_5': d['result_frame_5'],
                             'result_frame_6': d['result_frame_6'], 'result_frame_7': d['result_frame_7'],
                             'result_frame_8': d['result_frame_8'], 'result_frame_9': d['result_frame_9'],
                             'result_frame_10': d['result_frame_10']})


def end_of_game(request):
    print("test")
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    game_frame = BowlingGame.objects.filter(GameId=a)
    total = BowlingGame.objects.filter(GameId=a).aggregate(Sum('Result'))['Result__sum']
    d, m = {}, 1 #This is just to save few lines. It's good in combination with 'eval' but at the end I have just dict instead of query which is bad
    for x in range(1, 11):
        d["result_frame_{0}".format(x)] = BowlingGame.objects.filter(GameId=a, Frame=m).aggregate(Sum('Result'))['Result__sum']
        m += 1

    # needed for the stats on the end page
    num_of_strikes = BowlingGame.objects.filter(GameId=a, StrikeSpareInfo='X').count()
    num_of_spares = BowlingGame.objects.filter(GameId=a, StrikeSpareInfo='/').count()
    num_of_rolls = 21 - BowlingGame.objects.filter(GameId=a, Time=None).count()
    time_first = BowlingGame.objects.filter(GameId=a, Time__lt=datetime.datetime.now()).order_by('Time').first().Time
    time_last = BowlingGame.objects.filter(GameId=a, Time__lt=datetime.datetime.now()).order_by('Time').last().Time
    time = time_last - time_first
    time = time.seconds
    best_frame_result = max(d.values())
    total_games = a
    print("secondtest")
    #return JsonResponse({'message': 'This is the end of your game!'})
    return render(request, 'end.html', eval(open("game/constants/render_dict_end.txt").read()))


def game_loop(request): #This is my dispatch function
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    first_roll = BowlingGame.objects.filter(GameId=a, Time=None).first()
    frame = first_roll.Frame
    roll = first_roll.FrameRow
    name_of_button = request.GET.get('button', '0')
    print(name_of_button)
    global button_name
    button_name = name_of_button

    if frame == 1 and roll == 1:
        player_turn_one()
    elif frame == 10:
        player_turn_last()
    else:
        result_frame = BowlingGame.objects.filter(GameId=a, Frame=frame).aggregate(Sum('Result'))['Result__sum']
        if result_frame == None:
            player_turn_one()
        else:
            player_turn_two()
    return redirect('/play/') #Redirect by using different method. It allows arguments to be passed though I need to look at this closer


def first_frame(): #Return random result for the first roll
    return (random.randint(0, 10))


def second_frame(old_score): #And then for the second
    return (random.randint(0, 10 - old_score))


def player_turn_one(): #This is for the first roll of the frame
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    frame = BowlingGame.objects.filter(GameId=a, Time=None).first().Frame
    score = first_frame()
    revisions = BowlingGame.objects.filter(GameId=a, StrikeSpare__gt=0)

    for i in revisions: #Revise the previous results
        i.Result += score
        i.StrikeSpare -= 1
        i.save()
    record = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=1)
    record.Result = score
    record.Time = datetime.datetime.now()
    if score == 10: #Check for Strike
        record.StrikeSpare = 2
        record.StrikeSpareInfo = 'X'
        next_record = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=2)
        next_record.Time = datetime.datetime.now()
        next_record.save()
    record.save()


def player_turn_two(): #This is the second roll
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    frame = BowlingGame.objects.filter(GameId=a, Time=None).first().Frame
    old_score = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=1).Result
    score = second_frame(old_score)
    revisions = BowlingGame.objects.filter(GameId=a, StrikeSpare__gt=0)

    for i in revisions: #Revisions of the result if any
        i.Result += score
        i.StrikeSpare -= 1
        i.save()
    record = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=2)
    record.Result = score
    record.Time = datetime.datetime.now()
    total_for_frame = old_score + score
    if total_for_frame == 10: #Check for spare
        record.StrikeSpare = 1
        record.StrikeSpareInfo = '/'
        record.save()
    record.save()


def player_turn_last(): #This is for the last frame.
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    first_roll = BowlingGame.objects.filter(GameId=a, Time=None).first()
    frame = first_roll.Frame
    roll = first_roll.FrameRow

    if roll == 1: #First roll
        score = first_frame()
        revisions = BowlingGame.objects.filter(GameId=a, StrikeSpare__gt=0)
        for i in revisions:
            i.Result += score
            i.StrikeSpare -= 1
            i.save()
        record = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=1)
        record.Result = score
        record.Time = datetime.datetime.now()
        if score == 10:
            record.StrikeSpare = 2
            record.StrikeSpareInfo = 'X'
        record.save()
    if roll == 2: #Second Roll
        old_record = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=1).Result
        if old_record == 10:
            score = first_frame()
            revisions = BowlingGame.objects.filter(GameId=a, StrikeSpare__gt=0)
            for i in revisions:
                i.Result += score
                i.StrikeSpare -= 1
                i.save()
            record = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=2)
            record.Result = score
            record.Time = datetime.datetime.now()
            if score == 10:
                record.StrikeSpare = 1
                record.StrikeSpareInfo = 'X'
                record.save()
            record.save()
        if old_record < 10:
            old_score = old_record
            score = second_frame(old_score)
            revisions = BowlingGame.objects.filter(GameId=a, StrikeSpare__gt=0)
            for i in revisions:
                i.Result += score
                i.StrikeSpare -= 1
                i.save()
            record = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=2)
            record.Result = score
            record.Time = datetime.datetime.now()
            total_for_frame = old_score + score
            if total_for_frame == 10:
                record.StrikeSpare = 1
                record.StrikeSpareInfo = '/'
                record.save()
            if total_for_frame < 10:
                record.StateOfGame = 2
                record.save()
    if roll == 3: #And last
        score = first_frame()
        revisions = BowlingGame.objects.filter(GameId=a, StrikeSpare__gt=0)
        for i in revisions:
            i.Result += score
            i.StrikeSpare -= 1
            i.save()
        record = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=3)
        record.Result = score
        record.Time = datetime.datetime.now()
        record.StateOfGame = 2
        record.save()