from django.db import models


# Create your models here.


class SchoolProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='school logos/')

    def __str__(self):
        return self.name


class Player(models.Model):
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='players/')
    national_id = models.CharField(max_length=50, unique=True)
    national_id_image = models.FileField(upload_to='national ids/')
    birth_certificate = models.FileField(upload_to='certificates/')
    grade_7_result = models.FileField(upload_to='results/')
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.school.name}"


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
