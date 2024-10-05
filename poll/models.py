from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Poll(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=500)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100, null=True, blank=True)
    option_4 = models.CharField(max_length=100, null=True, blank=True)
    vote_count_opt1 = models.IntegerField(default=0)
    vote_count_opt2 = models.IntegerField(default=0)
    vote_count_opt3 = models.IntegerField(default=0)
    vote_count_opt4 = models.IntegerField(default=0)
    total_vote_count = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    

    def calculate_total_votes(self):
        total_votes = (
            self.vote_count_opt1 + self.vote_count_opt2 +
            (self.vote_count_opt3 or 0) + (self.vote_count_opt4 or 0)
        )
        return total_votes

    def save(self, *args, **kwargs):
        self.total_vote_count = self.calculate_total_votes()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question
    

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    selected_option = models.IntegerField()  