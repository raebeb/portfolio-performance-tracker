from django.core.management.base import BaseCommand
from ...services.load_excel import load_excel_data

class Command(BaseCommand):
    help = "Load data from an Excel file into the database"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help="path to the Excel file")

    def handle(self, *args, **options):
        filepath = options["filepath"]
        load_excel_data(filepath)
