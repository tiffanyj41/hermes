# recognized sections and their items
REQ_UV_HEADINGS = ("user_vector_data", "user_vector_transformations")
UV_HEADINGS = () + REQ_UV_HEADINGS + ("user_vector_schemas",) 

REQ_CV_HEADINGS = ("content_vector_data", "content_vector_transformations")
CV_HEADINGS = () + REQ_CV_HEADINGS + ("content_vector_schemas",)

DATASETS_HEADINGS = ("dataname",) + UV_HEADINGS + CV_HEADINGS

HEADINGS = { "datasets": DATASETS_HEADINGS, \
             "recommenders": ("recommenders"), \
             "metrics": ("metrics") \
            }

def map_section(config_parser, section):
    """ Map a section with the given section name and return a dictionary of the section.

    Args:
        config_parser: config parser of the configuration file
        section: section name to map

    Returns:
        section_dict: a dictionary of the section. 
        Use section_dict to obtain the value of the item provided that you know the item name, ie. section_dict[item_name].
    """

    section_dict = {}
    options = config_parser.options(section)
    for option in options:
        try:
            section_dict[option] = config_parser.get(section, option)
            if section_dict[option] == -1:
                Globals.logger.debug(__name__ + ": map_section(): skipping option " + option)
        except: 
            Globals.logger.error(__name__ + ": map_section(): exception on option " + option)
            section_dict[option] = None
    return section_dict
