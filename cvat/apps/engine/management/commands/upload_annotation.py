import json
import xmltodict

from django.core.management.base import BaseCommand
from ... import annotation
from ...log import slogger


class Command(BaseCommand):
    help = 'Uploads an XML File for a specific task'

    def add_arguments(self, parser):
        parser.add_argument('--tid', type=int)
        parser.add_argument('--xml_path', type=str)

    def handle(self, *args, **options):

        print(options['tid'])

        # delete old annotations
        try:
            slogger.task[options['tid']].info("delete annotation request")
            annotation.clear_task(options['tid'])
        except Exception:
            slogger.task[options['tid']].error("cannot delete annotation", exc_info=True)

# with open("output.json", 'w') as f:
#     f.write(jsonString)

        try:
            slogger.task[options['tid']].info("save annotation request")
            with open(options['xml_path'], 'r') as f:
                xml_dict = xmltodict.parse(f.read())
                print(xml_dict)
                json_str = json.dumps(xml_dict, indent=4)
                annotation.save_task(options['tid'], json_str)

        except Exception:
            slogger.task[options['tid']].error("cannot save annotation", exc_info=True)
