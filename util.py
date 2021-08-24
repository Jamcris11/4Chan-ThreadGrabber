# Splits the array into two so that both threads can handle a portion
def split_array(array):
    midpoint = len(array)//2
    return array[:midpoint], array[midpoint:]


def file_name_from_url(url):
	return url[url.rfind("/")+1:]