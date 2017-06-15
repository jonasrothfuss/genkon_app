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
      pk=int(record['pk']),
      question=Question.objects.get(pk=int(record['question_fk'])),
      choice_text=record['choice_text']
    ) for _, record in df.iterrows()]
    Choice.objects.bulk_create(choice_objects)

class Service(models.Model):
  service_name = models.CharField(max_length=80)
  service_link = models.CharField(max_length=400)
  service_title = models.CharField(max_length=80)
  service_subtitle = models.CharField(max_length=200)
  service_description = models.CharField(max_length=2000)
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
  date_posted = models.DateField("Datum", default=timezone.now)
  first_name = models.CharField("Vorname", max_length=30)
  last_name = models.CharField("Nachname", max_length=50)
  email = models.EmailField("E-Mail")
  phone_number = models.CharField("Telefonnummer", max_length=20, blank=True)
  occupation = models.CharField("Beruf", max_length=40, blank=True)
  street = models.CharField("Adresse", max_length=100)
  zip_code = models.CharField("PLZ", max_length=10)
  city = models.CharField("Stadt", max_length=40)
  message = models.TextField("Persönliche Nachricht", blank=True)
  selected_service = models.ForeignKey(Service, verbose_name="Gewähltes Ehrenamt", on_delete=models.SET_NULL, blank=True, null=True)
  empty_profile = models.BooleanField("Dummyprofil", default=False)
  accepted_terms = models.BooleanField("Einverständnis", default=False)
  deleted = models.BooleanField("Gelöscht", default=False)
  assigned = models.CharField("Im Einsatz bei", max_length=100, blank=True)
  remarks = models.TextField("Bearbeitungsnotizen", blank=True)


  def __str__(self):
    return self.first_name + " " + self.last_name

  @staticmethod
  def get_df(empty_profiles=True, choice_slection=True):
    if empty_profiles:
      profiles = Profile.objects.all()
    else:
      profiles = Profile.objects.filter(empty_profile=False)
    df = pd.DataFrame.from_records(profiles.values())

    # rename and reorder df columns
    col_name_replace_dict = dict([(field.name, field.verbose_name) for field in Profile._meta.local_fields])
    del col_name_replace_dict['selected_service']
    col_name_replace_dict['selected_service_id'] = 'Gewählter Service'
    df.rename(columns=col_name_replace_dict, inplace=True)
    df = df[['ID', 'Vorname', 'Nachname', 'Beruf', 'Gewählter Service', 'E-Mail', 'Telefonnummer', 'Adresse', 'Stadt', 'PLZ', 'Persönliche Nachricht', 'Dummyprofil']]

    #replace selected_service_ids with service names
    df['Gewählter Service'] = retrieve_service_names(df['Gewählter Service'])

    if choice_slection:
      choice_selection_df = Profile_Choice_Selection.get_profile_choices_as_df()
      df = df.merge(choice_selection_df,  left_on='ID', right_index=True)
    return df

  @staticmethod
  def create_empty_profile():
    return Profile(first_name="", last_name="", email="empty@empty", street="", zip_code="", city="", empty_profile = True)

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

  @staticmethod
  def get_profile_choices_as_df():
    profiles = Profile.objects.all()
    choices = Choice.objects.all()
    profile_choice_dict = {}
    for choice in choices:
      choice_bool_array = []
      for profile in profiles:
        try:
          choice_bool_array.append(Profile_Choice_Selection.objects.get(profile=profile, choice=choice).selected)
        except:
          choice_bool_array.append(False)
      profile_choice_dict[choice.choice_text] = choice_bool_array
    df = pd.DataFrame.from_dict(profile_choice_dict)
    df.index = [profile.id for profile in profiles]
    return df

def generate_service_choice_scores_randomly():
  services = Service.objects.all()
  choices = Choice.objects.all()
  for s in services:
    for c in choices:
      Service_Choice_Score(service=s, choice=c, score=np.random.randint(-3,3)).save()

def df_from_csv(csv_dir, model, expected_cols = []):
  csv_file = glob.glob(os.path.join(csv_dir, '*' + str(model) + '*.csv'))[0]
  for sep in [',', ';', '\t']:
    try:
      df = pd.read_csv(csv_file, sep = sep)
      assert set(df.columns) >= set(expected_cols)
      return df
    except Exception as e:
      if sep =='\t':
        raise AssertionError("Could not parse CSV properly - expected the following columns:" + str(expected_cols))

def load_data_from_csv(csv_dir):
  image_dir = os.path.join(csv_dir, 'images')
  Question.save_df_data(df_from_csv(csv_dir, 'Question', ['pk', 'question_identifier', 'question_text', 'question_type']))
  print('--- SAVED QUESTIONS SUCCESSFULLY')

  Choice.save_df_data(df_from_csv(csv_dir, 'Choice', ['pk', 'question_fk', 'choice_text']))
  print('--- SAVED CHOICES SUCCESSFULLY')

  Service.save_df_data(df_from_csv(csv_dir, 'Service', ['pk', 'service_name', 'service_link', 'service_title', 'service_subtitle',
                                   'service_description', 'service_urgency', 'service_unsalaried', 'service_image']), image_dir)
  print('--- SAVED SERVICES SUCCESSFULLY')

  Service_Choice_Score.save_df_data(df_from_csv(csv_dir, 'Score', ['pk', 'service_fk', 'choice_fk', 'score']))
  print('--- SAVED SCORES SUCCESSFULLY')

  print('Data successfully stored in the database')

def retrieve_service_names(service_ids):
  service_names = []
  for service_id in service_ids:
    if np.isnan(service_id):
      service_names.append('')
    else:
      try:
        service_names.append(Service.objects.get(pk=int(service_id)).service_name)
      except:
        service_names.append('')
  return service_names
