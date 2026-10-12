from action_db import get_all_public_texts
from rapidfuzz import fuzz, utils

all_public_texts = get_all_public_texts()


def evaluate_public_text(query: str, text: object) -> float:

    title_score = fuzz.token_set_ratio(query, text.title, processor= utils.default_process)
    category_score = fuzz.token_set_ratio(query, text.category, processor= utils.default_process)
    tags_score = fuzz.token_set_ratio(query, text.tags, processor= utils.default_process)

    weight_title = title_score * 0.6
    weight_category = category_score * 0.3
    weight_tags = tags_score * 0.1
 
    return weight_title + weight_category + weight_tags


def smart_search(query: str, texts: list[object], score_cutoff= 60) -> list[object]:

    sorted_texts = sorted(texts, key= lambda i: evaluate_public_text(query, i), reverse= True)
    filtred_texts = filter(lambda i: evaluate_public_text(query, i) > score_cutoff, sorted_texts)
    return filtred_texts

def print_to_check_smart_search(query: str, texts: list[object], score_cutoff= 40):
    search_results = smart_search(query, texts, score_cutoff)

    for pos, result in enumerate(search_results, start= 1):
        print(f"{pos}. {result.title}")
