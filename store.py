import pickle
from pathlib import Path
import numpy as np


class VectorStore:
    def __init__(self, base_dir: str = ".simply_index") -> None:
        self.base_dir = Path(base_dir).resolve()

        if not self.base_dir.exists():
            old = Path("index_data").resolve()
            if old.exists():
                old.rename(self.base_dir)
                print(f"📦 Migrated index_data → {self.base_dir.name}")

        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.vectors: np.ndarray | None = None
        self.entries: list[dict] = []

    def add(self, vectors: np.ndarray, entries: list[dict]) -> None:
        if len(vectors) != len(entries):
            raise ValueError(
                f"length mismatch: got {len(vectors)} vectors but {len(entries)} entries"
            )
        new = np.asarray(vectors, dtype=np.float32)
        if self.vectors is None:
            self.vectors = new
        else:
            self.vectors = np.vstack([self.vectors, new])
        self.entries.extend(entries)

    def save(self) -> None:
        np.save(self.base_dir / "vectors.npy", self.vectors)
        with open(self.base_dir / "entries.pkl", "wb") as f:
            pickle.dump(self.entries, f)

    def load(self) -> None:
        vpath = self.base_dir / "vectors.npy"
        epath = self.base_dir / "entries.pkl"
        if not vpath.exists():
            raise FileNotFoundError(
                f"Index not found at {vpath} — run `index` first"
            )
        if not epath.exists():
            raise FileNotFoundError(
                f"Entries not found at {epath} — index is corrupt, re-run `index`"
            )
        self.vectors = np.load(vpath)
        with open(epath, "rb") as f:
            self.entries = pickle.load(f)

    def search(
        self, query_vector: np.ndarray, top_k: int = 3
    ) -> list[dict]:
        if self.vectors is None:
            raise ValueError("Index empty — call add() then save(), or load() first.")
        q = np.asarray(query_vector, dtype=np.float32)
        if q.shape != (self.vectors.shape[1],):
            raise ValueError(
                f"query shape {q.shape} does not match vector dimension {self.vectors.shape[1]}"
            )
        q_norm = q / np.linalg.norm(q)
        v_norms = self.vectors / np.linalg.norm(self.vectors, axis=1, keepdims=True)
        sims = v_norms @ q_norm
        top_idx = sims.argsort()[::-1][:top_k]
        return [
            {"entry": self.entries[int(i)], "score": float(sims[i])}
            for i in top_idx
        ]

    def __len__(self) -> int:
        return len(self.entries)

    def __repr__(self) -> str:
        n = len(self.entries) if self.vectors is not None else 0
        return f"VectorStore(base_dir={self.base_dir!r}, n={n})"
