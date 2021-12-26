from .general.annotated_word import AnnotatedWord
from .general.patterns_populator_ng import _populate_pattern, _preprocess_population
from typing import List, Tuple, Dict
from utils import Language, GeneratedSentence
from joblib import Parallel, delayed
from cache_manager.manager import CacheOptions, g_cache_manager

class PopulateTask:

    def __init__(self, raw_pattern : str, lang : Language, idx : int) -> None:
        self.raw_pattern = raw_pattern
        self.lang = lang
        self.idx = idx
        self.generated_sentences : List[str] = None
        self.parsed_words : List[AnnotatedWord] = None


def populate_pattern(populate_task : PopulateTask):

    populate_task.generated_sentences = _populate_pattern(populate_task.parsed_words, populate_task.lang)
    return populate_task

def resolve_disambiguity(populated_tasks : List[PopulateTask], cache_exists_ok=False):

    g_cache_manager.start_caching(CacheOptions.DISAMBIGUITY, exists_ok=cache_exists_ok)
    for task in populated_tasks:
        task.parsed_words = _preprocess_population(task.raw_pattern, task.lang)
    g_cache_manager.end_caching(CacheOptions.DISAMBIGUITY)
    return populated_tasks

def get_population_tasks(sentence_pairs: List[Tuple[str, str]], src: Language, dest: Language):
    
    population_tasks : List[PopulateTask] = []
    for idx, (src_sent, dest_sent)  in enumerate(sentence_pairs):
        population_tasks.append(PopulateTask(src_sent, src, idx))
        population_tasks.append(PopulateTask(dest_sent, dest, idx))
    
    return population_tasks

def reorder_tasks(tasks : List[PopulateTask], num_patterns : int, src : Language) -> Tuple[List[Dict], List[Dict]] :

    src_sentences = [None] * num_patterns
    dest_senteces = [None] * num_patterns 
    for task in tasks:
        if task.lang == src:
            src_sentences[task.idx] = task.generated_sentences
        else:
            dest_senteces[task.idx] = task.generated_sentences
    return src_sentences, dest_senteces

def validate_population(src_sentences : List[Dict], dest_sentences : List[Dict], sentences_pairs):

    src_text_to_translate = []
    dest_reference = []
    src_orig_sentences = []

    for i, (src_sentences, dest_sentences) in enumerate(zip(src_sentences, dest_sentences)):
        assert len(src_sentences) == len(dest_sentences), f"pattern: {i+1}\n {src_sentences}\n{dest_sentences}\n" \
                                                                f"{src_sentences}\n{dest_sentences}"
        # TODO explain why there are duplicates.
        
        unique_pairs = set()
        for meta, sentence in src_sentences.items():
            unique_pairs.add((sentence, dest_sentences[meta]))

        src_pattern = sentences_pairs[i][0]
        dest_pattern = sentences_pairs[i][1]
        src_sentences = [pair[0] for pair in unique_pairs]
        dest_sentences = [GeneratedSentence(pair[1].lower(), dest_pattern, src_pattern) for pair in unique_pairs]

        src_text_to_translate.extend(src_sentences)
        dest_reference.extend(dest_sentences)
        src_orig_sentences.extend(src_sentences)

    return src_text_to_translate, dest_reference, src_orig_sentences

def populate(sentence_pairs: List[Tuple[str, str]], src: Language, dest: Language, remove_disambguity_cache : bool):

    tasks = get_population_tasks(sentence_pairs, src, dest)
    tasks =  resolve_disambiguity(tasks, remove_disambguity_cache)
    tasks = Parallel(n_jobs=-1, verbose=50)(delayed(populate_pattern)(t) for t in tasks)
    src_sentences, dest_sentences = reorder_tasks(tasks, num_patterns=len(sentence_pairs), src=src)
    return validate_population(src_sentences, dest_sentences, sentence_pairs)

    
