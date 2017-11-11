import sys, os
from django.core.management.base import BaseCommand, CommandError
from survey.models import *

class Command(BaseCommand):
  help = 'Clears the database and loads the data provided in the csv'

  def add_arguments(self, parser):
    parser.add_argument('csv_dir', nargs='+', type=str)

  def handle(self, *args, **options):
    assert 'csv_dir' in options
    load_data_from_csv(options['csv_dir'][0])
    self.stdout.write(self.style.SUCCESS('Successfully loaded the csv data from ' + str(options['csv_dir'][0])))