from django.db import models

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    type = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True)
    shop = models.CharField(max_length=128)
    link = models.URLField(max_length=254)
    image = models.URLField(max_length=254) 
    def __str__(self):
        return self.name

class GameData(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.game.name + ' datas - ' + str(self.date.strftime("%b %d %Y %H:%M:%S") )