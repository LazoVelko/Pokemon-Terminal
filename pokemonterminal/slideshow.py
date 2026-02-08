import atexit
import multiprocessing
import random

from .platform import PlatformNamedEvent
from threading import Thread

def __event_listener(event):
    event.wait()

def __get_listener_thread(event):
    t = Thread(target=__event_listener, args=(event, ), daemon=True)
    t.start()
    return t

def __slideshow_worker(filtered, delay, changer_func, event_name):
    with PlatformNamedEvent(event_name) as e:
        t = __get_listener_thread(e)
        random.shuffle(filtered)
        queque = iter(filtered)
        while t.is_alive():
            next_pkmn = next(queque, None)
            if next_pkmn is None:
                random.shuffle(filtered)
                queque = iter(filtered)
                continue
            changer_func(next_pkmn.get_path())
            t.join(delay * 60)

def start(filtered, delay, changer_func, event_name):
    p = multiprocessing.Process(target=__slideshow_worker, args=(filtered, delay, changer_func, event_name, ), daemon=True)
    p.start()
    # HACK remove multiprocessing's exit handler to prevent it killing our child.
    atexit.unregister(multiprocessing.util._exit_function)
    return p.pid

def stop(event_name):
    with PlatformNamedEvent(event_name) as e:
        e.signal()
