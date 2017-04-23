from django.db import models


class Question(models.Model):
  question_text = models.CharField(max_length=200)
  question_type = models.CharField(max_length=20, blank=True)

  def __str__(self):
    return self.question_text

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
  date_posted = models.DateField()
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=50)
  email = models.EmailField()
  phone_number = models.CharField(max_length=20)
  occupation = models.CharField(max_length=40)
  street = models.CharField(max_length=100)
  zip_code = models.CharField(max_length=10)
  city = models.CharField(max_length=40)
  message = models.CharField(max_length=1000)

  def __str__(self):
    return self.first_name + " " + self.last_name

class Service_Choice_Scores(models.Model):
  service = models.ForeignKey(Service, on_delete=models.CASCADE)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
  score = models.IntegerField()

class Profile_Choice_Selection(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
  selected = models.BooleanField()