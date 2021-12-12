import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
from enum import Enum

from utils import GeneratedSentence


class CacheOptions(Enum):
    DISAMBIGUITY = 1
    GOOGLE_COULD_AUTH = 2
    GEN_SENTENCES = 3
    TRANSLATED_SENTENCES = 4

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

        raise ValueError(f"{CacheOptions.GOOGLE_COULD_AUTH.name} is not cached")
    
    def cache_generated_sentences(self, src_sentences : List[str], dest_sentences : List[GeneratedSentence]):
        self.start_caching(CacheOptions.GEN_SENTENCES)
        self.caches_in_progress[CacheOptions.GEN_SENTENCES]['src'] = json.dumps(src_sentences)
        self.caches_in_progress[CacheOptions.GEN_SENTENCES]['dest'] = json.dumps([json.dumps(dest_sen.__dict__) for dest_sen in dest_sentences])
        self.end_caching(CacheOptions.GEN_SENTENCES)

    def load_generated_sentences(self) -> Tuple[List[str], List[GeneratedSentence]]:

        if CacheOptions.GEN_SENTENCES in self.caches:
            src = json.loads(self.caches[CacheOptions.GEN_SENTENCES]['src'])
            # GeneratedSentence obj is being serialized to dict when saved to JSON

            dest = [
                    GeneratedSentence(**json.loads(str_obj))
                    for str_obj in json.loads(self.caches[CacheOptions.GEN_SENTENCES]['dest']) 
                    ]
            return src, dest 

        raise ValueError(f"{CacheOptions.GEN_SENTENCES.name} is not cached")

    def cache_translated_sentences(self, translted_sentences : List[str]):
        self.start_caching(CacheOptions.TRANSLATED_SENTENCES)
        self.caches_in_progress[CacheOptions.TRANSLATED_SENTENCES]['translated'] = json.dumps(translted_sentences)
        self.end_caching(CacheOptions.TRANSLATED_SENTENCES)

    def load_translated_sentences(self) -> List[str]:

        if CacheOptions.TRANSLATED_SENTENCES in self.caches:
            return json.loads(self.caches[CacheOptions.TRANSLATED_SENTENCES]['translated'])
        raise ValueError(f"{CacheOptions.TRANSLATED_SENTENCES.name} is not cached")



# singelton
g_cache_manager = CacheManager()
