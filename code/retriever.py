import math
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

TOKEN_RE = re.compile(r"[a-zA-Z0-9]{2,}")


class CorpusRetriever:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.documents = self._load_documents()
        self.doc_vectors, self.idf = self._build_index(self.documents)

    def _load_documents(self) -> List[Dict[str, str]]:
        docs: List[Dict[str, str]] = []
        if not self.data_dir.exists():
            return docs
        for file_path in sorted(self.data_dir.glob("**/*")):
            if file_path.is_file() and file_path.suffix.lower() in {".txt", ".md"}:
                text = file_path.read_text(encoding="utf-8", errors="ignore").strip()
                if text:
                    docs.append({"source": str(file_path), "text": text})
        return docs

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in TOKEN_RE.findall(text)]

    def _build_index(self, docs: List[Dict[str, str]]):
        doc_term_counts = []
        df = Counter()
        for doc in docs:
            tokens = self._tokenize(doc["text"])
            counts = Counter(tokens)
            doc_term_counts.append(counts)
            df.update(counts.keys())

        n_docs = max(len(docs), 1)
        idf = {term: math.log((1 + n_docs) / (1 + freq)) + 1.0 for term, freq in df.items()}

        vectors = []
        for counts in doc_term_counts:
            vectors.append({term: tf * idf.get(term, 1.0) for term, tf in counts.items()})

        return vectors, idf

    def _vectorize_query(self, query: str) -> Dict[str, float]:
        counts = Counter(self._tokenize(query))
        return {term: tf * self.idf.get(term, 1.0) for term, tf in counts.items()}

    @staticmethod
    def _cosine_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
        if not v1 or not v2:
            return 0.0
        dot = sum(value * v2.get(term, 0.0) for term, value in v1.items())
        norm1 = math.sqrt(sum(v * v for v in v1.values()))
        norm2 = math.sqrt(sum(v * v for v in v2.values()))
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        return dot / (norm1 * norm2)

    def retrieve(self, query: str, top_k: int = 3) -> Tuple[List[Dict[str, str]], float]:
        if not self.documents:
            return [], 0.0

        qvec = self._vectorize_query(query)
        scored = []
        for idx, dvec in enumerate(self.doc_vectors):
            score = self._cosine_similarity(qvec, dvec)
            if score > 0:
                scored.append((score, idx))

        scored.sort(reverse=True)
        top = scored[:top_k]
        results = [
            {
                "source": self.documents[idx]["source"],
                "text": self.documents[idx]["text"],
                "score": f"{score:.4f}",
            }
            for score, idx in top
        ]
        confidence = top[0][0] if top else 0.0
        return results, confidence
