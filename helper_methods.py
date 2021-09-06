import random 
import string
import dbUtils


def generate_id(N):
    return_str = ''.join(random.choices(string.ascii_letters + string.digits, k=N))
    dbUtils.check_hash(return_str)
    return return_str

def format_url(url):
    url = url.lower()
    url.replace("http://", "")
    url.replace("http:", "")
    url.replace("http:/", "")
    url.replace("ht", "")
    url.replace("htt", "")
    url.replace("http", "")
    url.replace("https://", "")
    url.replace("www", "")
    return url



