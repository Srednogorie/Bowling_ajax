from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max
from django.db.models import Sum
from game.models import BowlingGame
from .serializers import BowlingGameSerializer
import datetime
import random
# Create your views here.


class BowlingGameModelView(generics.ListAPIView):
    queryset = BowlingGame.objects.all()
    serializer_class = BowlingGameSerializer


class BowlingGameGameView(generics.ListAPIView):
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    queryset = BowlingGame.objects.filter(GameId=a)
    serializer_class = BowlingGameSerializer


@api_view()
def total_score(request):
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    total = BowlingGame.objects.filter(GameId=a).aggregate(Sum('Result'))['Result__sum']
    return Response({"total_score": total})


@api_view()
def start_game(request):
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max'] + 1
    BowlingGame.objects.bulk_create(eval(open("game/constants/bulk_list.txt").read()))
    return Response({'message': 'You just started a new game. Please use the following link to roll the bow!'})


@api_view()
def game_loop(request):
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    first_roll = BowlingGame.objects.filter(GameId=a, Time=None).first()
    frame = first_roll.Frame
    roll = first_roll.FrameRow
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
    game_frame = BowlingGameSerializer(BowlingGame.objects.filter(GameId=a), many=True).data
    total = BowlingGame.objects.filter(GameId=a).aggregate(Sum('Result'))['Result__sum']
    exit = BowlingGame.objects.filter(GameId=a).aggregate(Max('StateOfGame'))['StateOfGame__max']
    if exit == 1:
        return Response({'message': 'You just rolled the bow!', 'game_frame': game_frame, 'total': total,
                         'state_of_game': exit})
    else:
        return Response({'message': 'This is the end of your game! Please look at some' +
                                    'statistics about your game!', 'game_frame': game_frame, 'total': total,
                         'state_of_game': exit})



def first_frame():
    return (random.randint(0, 10))


def second_frame(old_score):
    return (random.randint(0, 10 - old_score))


def player_turn_one():
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    frame = BowlingGame.objects.filter(GameId=a, Time=None).first().Frame
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
        next_record = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=2)
        next_record.Time = datetime.datetime.now()
        next_record.save()
    record.save()


def player_turn_two():
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    frame = BowlingGame.objects.filter(GameId=a, Time=None).first().Frame
    old_score = BowlingGame.objects.get(GameId=a, Frame=frame, FrameRow=1).Result
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
    record.save()


def player_turn_last():
    a = BowlingGame.objects.all().aggregate(Max('GameId'))['GameId__max']
    first_roll = BowlingGame.objects.filter(GameId=a, Time=None).first()
    frame = first_roll.Frame
    roll = first_roll.FrameRow

    if roll == 1:
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
    if roll == 2:
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
    if roll == 3:
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