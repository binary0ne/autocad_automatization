import functions as tools
from settings import Settings
from blueprint import Blueprint

# Load settings
settings = Settings()

# Check and create json file if not exist
if tools.check_file(settings.temp_file) == False:
	tools.parse(settings.input_file, settings.temp_file)

# Load dictionary of objects
array = tools.load(settings.temp_file)

# Create blueprint out of objects
bp = Blueprint(array)

# Check and create geometry lines file if not exist
if tools.check_file(settings.lines_file) == False:
	bp.generate_lines()
	tools.dump(bp.lines, settings.lines_file)
else:
	bp.lines = tools.load(settings.lines_file)

bp.count_objects()
bp.find_refferences()
# bp.vizualize_lines()
bp.find_room("object_49477")
# bp.ping_radius([0,0], 5, 360)