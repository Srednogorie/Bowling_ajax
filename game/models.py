from django.db import models

# Create your models here.

class BowlingGame(models.Model):
    Frame = models.PositiveSmallIntegerField()
    FrameRow = models.PositiveSmallIntegerField()
    Result = models.PositiveSmallIntegerField(blank=True, null=True)
    StrikeSpare = models.PositiveSmallIntegerField(blank=True, null=True)
    StrikeSpareInfo = models.CharField(max_length=1, blank=True, null=True)
    Time = models.DateTimeField(blank=True, null=True)
    GameId = models.PositiveIntegerField()
    StateOfGame = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ('GameId',)

    def __str__(self):
        return str(self.GameId)