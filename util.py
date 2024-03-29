import html_parsing as HTML

# Splits the array into two so that both threads can handle a portion
def split_array(array):
    midpoint = len(array)//2
    return array[:midpoint], array[midpoint:]


def file_name_from_url(url):
	return url[url.rfind("/")+1:]


def four_chan_get_urls(html_parser):
    return HTML.parse_urls(html_parser.find_all(class_="fileThumb"))