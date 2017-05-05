from django.db import models
from django.utils import timezone
import os
import numpy as np
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import glob

fs = FileSystemStorage(location="static")

class Question(models.Model):
  question_identifier = models.CharField(max_length=10)
  question_text = models.CharField(max_length=200)
  question_type = models.CharField(max_length=20, blank=True)

  def __str__(self):
    return self.question_text

  def get_choices(self):
    return Choice.objects.filter(question=self)

  def get_choices_as_dict(self):
    choice_tuples = [c.choice_text.split('-') for c in self.get_choices()]
    choice_pks = [c.pk for c in self.get_choices()]
    assert all([len(t)==2 for t in choice_tuples])
    choice_dict = {}
    for (key, value), pk in zip (choice_tuples, choice_pks):
      if key in choice_dict.keys():
        choice_dict[key].append((pk, value))
      else:
        choice_dict[key] = [(pk, value)]
    return choice_dict

  def get_choice_options(self):
    return list(set([c.choice_text.split('-')[1] for c in self.get_choices()]))

  @staticmethod
  def save_df_data(df):
    assert set(df.columns) >= set(['pk', 'question_identifier', 'question_text', 'question_type'])
    df = df.replace(np.nan, '', regex=True)
    question_objects = [Question(
      pk=record['pk'],
      question_identifier=record['question_identifier'],
      question_text=record['question_text'],
      question_type=record['question_type']
    ) for _, record in df.iterrows()]
    Question.objects.bulk_create(question_objects)

class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=100)

  def __str__(self):
    return self.choice_text + " (" + self.question.question_text  + ")"

  @staticmethod
  def save_df_data(df):
    assert set(df.columns) >= set(['pk', 'question_fk', 'choice_text'])
    df = df.replace(np.nan, '', regex=True)
    choice_objects = [Choice(
      pk=record['pk'],
      question=Question.objects.get(pk=record['question_fk']),
      choice_text=record['choice_text']
    ) for _, record in df.iterrows()]
    Choice.objects.bulk_create(choice_objects)

class Service(models.Model):
  service_name = models.CharField(max_length=30)
  service_link = models.CharField(max_length=300)
  service_title = models.CharField(max_length=30)
  service_subtitle = models.CharField(max_length=100)
  service_description = models.CharField(max_length=300)
  service_urgency = models.IntegerField()
  service_unsalaried = models.BooleanField()
  service_image = models.ImageField(upload_to="services", storage=fs)

  def __str__(self):
    return self.service_name

  @staticmethod
  def save_df_data(df, image_dir):
    assert set(df.columns) >= set(['pk', 'service_name', 'service_link', 'service_title', 'service_subtitle',
                                   'service_description', 'service_urgency', 'service_unsalaried', 'service_image'])
    df['service_unsalaried'].map(lambda x: bool(x))
    df = df.replace(np.nan, '', regex=True)
    service_objects = []
    for _, record in df.iterrows():
      service = Service(pk=record['pk'],
        service_name=record['service_name'],
        service_link=record['service_link'],
        service_title=record['service_title'],
        service_subtitle=record['service_subtitle'],
        service_description=record['service_description'],
        service_urgency=int(record['service_urgency']),
        service_unsalaried=bool(record['service_unsalaried']),
      )
      service.service_image.save(record['service_image'],  File(open(os.path.join(image_dir, record['service_image']), 'rb')))
      service_objects.append(service)
    #Service.objects.bulk_create(service_objects)

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
  selected_service = models.ForeignKey(Service, verbose_name="Gewählter Service", on_delete=models.SET_NULL, blank=True, null=True)

  def __str__(self):
    return self.first_name + " " + self.last_name

class Service_Choice_Score(models.Model):
  service = models.ForeignKey(Service, on_delete=models.CASCADE)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
  score = models.IntegerField()

  @staticmethod
  def save_df_data(df):
    assert set(df.columns) >= set(['pk', 'service_fk', 'choice_fk', 'score'])
    score_objects = [Service_Choice_Score(
      pk=record['pk'],
      service=Service.objects.get(pk=record['service_fk']),
      choice=Choice.objects.get(pk=record['choice_fk']),
      score=int(record['score'])
    ) for _, record in df.iterrows()]
    Service_Choice_Score.objects.bulk_create(score_objects)

class Profile_Choice_Selection(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
  selected = models.BooleanField()

def generate_service_choice_scores_randomly():
  services = Service.objects.all()
  choices = Choice.objects.all()
  for s in services:
    for c in choices:
      Service_Choice_Score(service=s, choice=c, score=np.random.randint(-3,3)).save()

def make_model_df_dict(csv_dir, models = ['Question', 'Choice', 'Service', 'Score']):
  csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))
  model_df_dict = {}
  for model in models:
    csv_file = glob.glob(os.path.join(csv_dir, '*' + model + '*.csv'))[0]
    if model=='Service':
      model_df_dict[model] = pd.read_csv(csv_file, sep = '\t', lineterminator = '\n')
    else:
      model_df_dict[model] = pd.read_csv(csv_file)
  return model_df_dict

def load_data_from_csv(csv_dir):
  image_dir = os.path.join(csv_dir, 'images')
  model_df_dict = make_model_df_dict(csv_dir)
  Question.save_df_data(model_df_dict['Question'])
  Choice.save_df_data(model_df_dict['Choice'])
  Service.save_df_data(model_df_dict['Service'], image_dir)
  Service_Choice_Score.save_df_data(model_df_dict['Score'])
  print('Data successfully stored in the database')