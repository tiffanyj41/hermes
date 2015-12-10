import logging

REQ_UV_HEADINGS = ("user_vector_data", "user_vector_types")
UV_HEADINGS = () + REQ_UV_HEADINGS + ("user_vector_schemas",) 

REQ_CV_HEADINGS = ("content_vector_data", "content_vector_types")
CV_HEADINGS = () + REQ_CV_HEADINGS + ("content_vector_schemas",)

DATASETS_HEADINGS = ("vectorizer",) + UV_HEADINGS + CV_HEADINGS

HEADINGS = { "datasets": DATASETS_HEADINGS, \
	         "recommenders": ("recommenders"), \
	         "metrics": ("metrics") \
	        }

# get logger
logger = logging.getLogger("hermes")

def map_section(config_parser, section):
	global logger
	section_dict = {}
	options = config_parser.options(section)
	for option in options:
		try:
			section_dict[option] = config_parser.get(section, option)
			if section_dict[option] == -1:
				logger.debug(__name__ + ": map_section(): skipping option " + option)
		except: 
			logger.error(__name__ + ": map_section(): exception on option " + option)
			section_dict[option] = None
	return section_dict
