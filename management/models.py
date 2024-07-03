from django.db import models



# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField()
    participation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TournamentResults(models.Model):
    STAGE_CHOICES = [
        ('Group Stage', 'Group Stage'),
        ('Quarter Final', 'Quarter Final'),
        ('Semi Final', 'Semi Final'),
        ('Final', 'Final'),
    ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    school1 = models.ForeignKey('schools.SchoolProfile', related_name='school1', on_delete=models.CASCADE)
    school2 = models.ForeignKey('schools.SchoolProfile', related_name='school2', on_delete=models.CASCADE)
    school1_score = models.IntegerField()
    school2_score = models.IntegerField()
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    results_file = models.FileField(upload_to='results/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tournament.name}: {self.school1.name} vs {self.school2.name} - {self.school1_score}:{self.school2_score} ({self.stage})"
