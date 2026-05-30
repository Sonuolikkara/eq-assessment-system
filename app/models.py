from django.db import models

class Assessment(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    profession = models.CharField(max_length=100)
    scenario = models.TextField()
    response = models.TextField()
    sentiment_score = models.FloatField()
    eq_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.eq_score}"
