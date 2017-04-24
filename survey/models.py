from django.db import models
from django.utils import timezone


class Question(models.Model):
  question_identifier = models.CharField(max_length=10)
  question_text = models.CharField(max_length=200)
  question_type = models.CharField(max_length=20, blank=True)

  def __str__(self):
    return self.question_text

  def get_choices(self):
    return Choice.objects.filter(question=self)

class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=100)

  def __str__(self):
    return self.choice_text + " (" + self.question.question_text  + ")"

class Service(models.Model):
  service_name = models.CharField(max_length=30)
  service_link = models.CharField(max_length=300)
  service_title = models.CharField(max_length=30)
  service_subtitle = models.CharField(max_length=100)
  service_description = models.CharField(max_length=300)
  service_urgency = models.IntegerField()
  service_unsalaried = models.BooleanField()
  service_image = models.ImageField()

  def __str__(self):
    return self.service_name

class Profile(models.Model):
  date_posted = models.DateField("Erstellugsdatum", default=timezone.now)
  first_name = models.CharField("Vorname", max_length=30)
  last_name = models.CharField("Nachname", max_length=50)
  email = models.EmailField("E-Mail")
  phone_number = models.CharField("Telefonnummer", max_length=20, blank=True)
  occupation = models.CharField("Beruf", max_length=40, blank=True)
  street = models.CharField("Adresse", max_length=100)
  zip_code = models.CharField("PLZ", max_length=10)
  city = models.CharField("Stadt", max_length=40)
  message = models.TextField("Persönliche Nachricht", blank=True)

  def __str__(self):
    return self.first_name + " " + self.last_name

class Service_Choice_Score(models.Model):
  service = models.ForeignKey(Service, on_delete=models.CASCADE)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
  score = models.IntegerField()

class Profile_Choice_Selection(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
  selected = models.BooleanField()