import sys
# from web_scraping.indievox2 import get_indievox
# import threading
# thread_indievox = threading.Thread(target=get_indievox)
# thread_indievox.start()

from web_scraping.get_concert_info import get_latest_concert_info
import threading
thread_a = threading.Thread(target=get_latest_concert_info())
thread_a.start()