import json
from pathlib import Path
from typing import Dict
from enum import Enum


class CacheOptions(Enum):
    DISAMBIGUITY = 1
    GOOGLE_COULD_AUTH = 2

def path_to_cache(cache_option : CacheOptions):

    lower_case_name = cache_option.name.lower()
    return Path(__file__).parent.parent.absolute() / 'cache' / f"{lower_case_name}.json"
    

class CacheManager:

    def __init__(self) -> None:
        self.caches = None
        self.load_caches()
        self.caches_in_progress = dict()
        self.current_cache : Dict = None
        self.current_cache_name = None
    
    def load_caches(self):
        global_cache = {}
        for name in CacheOptions:
            path = path_to_cache(name)
            if path.exists():
                with path.open('r') as f:
                    global_cache[name] = json.load(f)
        self.caches = global_cache
    
    def start_caching(self, cache_name : CacheOptions, exists_ok=False):
        assert cache_name in CacheOptions, f"can't cache {cache_name}. supported caches - {[cache.name for cache in CacheOptions]}"
        if not exists_ok and cache_name in self.caches.keys():
            return
        if not cache_name in self.caches_in_progress.keys():
            self.caches_in_progress[cache_name] = dict()
    
    def end_caching(self, cache_name : CacheOptions):
        if cache_name in self.caches_in_progress.keys():
            self.caches[cache_name] = self.caches_in_progress[cache_name]
            path = path_to_cache(cache_name)
            path.parent.mkdir(exist_ok=True, parents=True)
            with path.open('w') as f:
                json.dump(self.caches_in_progress[cache_name], f)
            
            self.caches[cache_name] = self.caches_in_progress[cache_name]
            self.caches_in_progress.pop(cache_name)


    def cache_disambiguity(self, pattern : str, chosen_meaning_idx : int):
        if CacheOptions.DISAMBIGUITY in self.caches_in_progress.keys():
            self.caches_in_progress[CacheOptions.DISAMBIGUITY][pattern] = chosen_meaning_idx


    def load_disambiguity(self, pattern : str):

        if CacheOptions.DISAMBIGUITY in self.caches:
            if pattern in self.caches[CacheOptions.DISAMBIGUITY]:
                return self.caches[CacheOptions.DISAMBIGUITY][pattern]

        raise ValueError(f"Pattern {pattern} is not cached")
    
    def cache_google_auth(self, google_auth_path : str):
        self.start_caching(CacheOptions.GOOGLE_COULD_AUTH)
        self.caches_in_progress[CacheOptions.GOOGLE_COULD_AUTH][CacheOptions.GOOGLE_COULD_AUTH.name] = google_auth_path
        self.end_caching(CacheOptions.GOOGLE_COULD_AUTH)

    def load_google_auth(self):

        if CacheOptions.GOOGLE_COULD_AUTH in self.caches:
            return self.caches[CacheOptions.GOOGLE_COULD_AUTH][CacheOptions.GOOGLE_COULD_AUTH.name]

        raise ValueError(f"Google Cloud Auth is not cached")
    
    

# singelton
g_cache_manager = CacheManager()
