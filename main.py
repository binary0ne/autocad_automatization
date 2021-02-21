import functions as tools
from settings import Settings
from blueprint import Blueprint

settings = Settings()

if tools.check_file(settings.temp_file) == False:
	tools.parse(settings.input_file, settings.temp_file)

array = tools.load(settings.temp_file)

bp = Blueprint(array)

if tools.check_file(settings.lines_file) == False:
	bp.generate_lines()
	tools.dump(bp.lines, settings.lines_file)
else:
	bp.lines = tools.load(settings.lines_file)

bp.count_objects()
bp.find_refferences()

bp.vizualize_lines()