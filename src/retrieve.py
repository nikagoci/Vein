import math
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STOP = set("a an the is are of to in how what does do why can it and or for with on be by as at this that than work".split())


def tokens(text):
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    out = []
    for w in re.findall(r"[a-z0-9]+", text):
        if w in STOP:
            continue
        out.append(w[:-1] if len(w) > 3 and w.endswith("s") else w)
    return out


def load_chunks(corpus=None):
    corpus = corpus or ROOT / "data" / "corpus"
    chunks = []
    for p in sorted(Path(corpus).glob("*.md")):
        for para in re.split(r"\n\s*\n", p.read_text(encoding="utf-8")):
            para = para.strip()
            if para and not para.startswith("#"):
                chunks.append({"source": p.name, "text": para})
    return chunks


def retrieve(question, chunks, k=3):
    """Return up to k chunks with a score in [0, 1]: idf-weighted share of the
    question's words found in the chunk. Unknown words weigh the most, so
    off-topic questions score low."""
    q = set(tokens(question))
    if not q or not chunks:
        return []
    docs = [set(tokens(c["text"])) for c in chunks]
    n = len(docs)
    idf = {w: math.log((n + 1) / (sum(w in d for d in docs) + 0.5)) + 1 for w in q}
    total = sum(idf.values())
    scored = [dict(c, score=sum(idf[w] for w in q & d) / total) for c, d in zip(chunks, docs)]
    return sorted(scored, key=lambda h: -h["score"])[:k]
