import functions as tools
from settings import Settings
from blueprint import Blueprint

settings = Settings()

if tools.check_file(settings.temp_file) == False:
	tools.parse(settings.input_file, settings.temp_file)

array = tools.load(settings.temp_file)

bp = Blueprint(array)

bp.calculate_objects()

print(bp.objects_list)