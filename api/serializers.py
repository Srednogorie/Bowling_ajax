from rest_framework import serializers
from game.models import BowlingGame

class BowlingGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BowlingGame
        fields = ('Frame', 'FrameRow', 'Result', 'StrikeSpare', 'Time', 'GameId', 'StrikeSpareInfo', 'StateOfGame')