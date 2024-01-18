import json
import os
import threading

json_new = ['era_new.json,'
            'indievox_new.json',
            'kktix_new.json',
            'livenation_new.json',
            'ticketplus_new.json']

thread_era = threading.Thread(target=get_era)
thread_indievox = threading.Thread(target=get_indievox)
thread_kktix = threading.Thread(target=get_kktix)
thread_livenation = threading.Thread(target=get_livenation)
threading_ticketplus = threading.Thread(target=get_tixcraft)