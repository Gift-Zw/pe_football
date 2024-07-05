from datetime import datetime
from core.models import User
from django.db import models


# Create your models here.


class SchoolProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='school logos/')
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE)
    passport_photo = models.ImageField(upload_to='players/')
    national_id = models.CharField(max_length=50, unique=True)
    national_id_image = models.FileField(upload_to='national ids/')
    birth_certificate = models.FileField(upload_to='certificates/')
    grade_7_result = models.FileField(upload_to='results/')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, default='')
    birth_certificate_number = models.CharField(max_length=255)
    guardian_name = models.CharField(max_length=255)
    guardian_relationship = models.CharField(max_length=255)
    guardian_contact = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    present_school = models.CharField(max_length=255)
    year_enrolled = models.CharField(max_length=255)
    previous_school = models.CharField(max_length=255)
    cell = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.school.name}"

    @property
    def age(self):
        return datetime.today().year - self.date_of_birth.year


class TournamentRegistration(models.Model):
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE)
    tournament = models.ForeignKey('management.Tournament', on_delete=models.CASCADE)
    proof_of_payment = models.FileField(upload_to='proofs of payment/')
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.school.name} - {self.tournament.name}"


class TournamentPlayer(models.Model):
    tournament = models.ForeignKey('management.Tournament', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tournament', 'player')

    def __str__(self):
        return f"{self.player.name} - {self.tournament.name}"
