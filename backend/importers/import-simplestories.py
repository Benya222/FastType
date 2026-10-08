import time
import requests

from models import db, PublicText


API_URL = "https://datasets-server.huggingface.co/rows"

DATASET = "SimpleStories/SimpleStories"
CONFIG = "default"
SPLIT = "train"

BATCH_SIZE = 100

# Сколько текстов хотим импортировать.
MAX_TEXTS = 10_000

# Для typing trainer я бы пока брал тексты в этом диапазоне.
MIN_WORDS = 30
MAX_WORDS = 250


def fetch_batch(offset: int, length: int = BATCH_SIZE) -> list[dict]:
    params = {
        "dataset": DATASET,
        "config": CONFIG,
        "split": SPLIT,
        "offset": offset,
        "length": length,
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    return response.json()["rows"]


def make_title(data: dict) -> str:
    topic = data.get("topic") or "Story"
    theme = data.get("theme")

    if theme:
        return f"{topic.title()} — {theme.title()}"

    return topic.title()


def make_category(data: dict) -> str:
    return (data.get("topic") or "Other").strip()


def make_tags(data: dict) -> str:
    tags = []

    for field in ("topic", "theme", "style", "feature", "grammar"):
        value = data.get(field)

        if value and value.strip():
            tags.append(value.strip())

    # Убираем дубликаты, сохраняя порядок.
    tags = list(dict.fromkeys(tags))

    # Например:
    # "talking animals, Perseverance, playful, symbolism"
    return ", ".join(tags)


def import_texts():
    imported = 0
    offset = 3000

    while imported < MAX_TEXTS:
        print(f"Fetching rows {offset}–{offset + BATCH_SIZE}...")

        rows = fetch_batch(offset)

        if not rows:
            print("No more rows.")
            break

        for row in rows:
            data = row["row"]

            text = (data.get("story") or "").strip()
            word_count = data.get("word_count") or 0
            char_count = data.get("character_count") or len(text)

            # Отбрасываем слишком короткие/длинные тексты.
            if word_count < MIN_WORDS:
                continue

            if word_count > MAX_WORDS:
                continue

            # generation_id есть в SimpleStories и хорошо подходит
            # в качестве уникального идентификатора источника.
            source_id = data.get("generation_id")

            if source_id:
                exists = (
                    PublicText
                    .select()
                    .where(PublicText.source_id == source_id)
                    .exists()
                )

                if exists:
                    continue

            PublicText.create(
                title=make_title(data),
                text=text,
                category=make_category(data),
                tags=make_tags(data),
                char_count=char_count,
                word_count=word_count,
                source_id=source_id,
            )

            imported += 1

            if imported >= MAX_TEXTS:
                break

        offset += len(rows)

        print(f"Imported: {imported}/{MAX_TEXTS}")

        # Не надо долбить API слишком быстро.
        time.sleep(2)

# last offset - 19400 | next offset 19500 
if __name__ == "__main__":
    db.connect(reuse_if_open=True)
    db.create_tables([PublicText])
    try:
        import_texts()
    finally:
        if not db.is_closed():
            db.close()