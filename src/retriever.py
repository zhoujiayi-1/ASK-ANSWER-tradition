import json
import jieba
from rank_bm25 import BM25Okapi

class BM25Retriever:
    def __init__(self, knowledge_base_path):
        self.knowledge_base_path = knowledge_base_path
        self.documents = self._load_documents()
        self.tokenized_docs = [list(jieba.cut(doc['content'])) for doc in self.documents]
        self.bm25 = BM25Okapi(self.tokenized_docs)
    
    def _load_documents(self):
        documents = []
        with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    documents.append(json.loads(line))
        return documents
    
    def retrieve(self, query, top_k=5):
        tokenized_query = list(jieba.cut(query))
        scores = self.bm25.get_scores(tokenized_query)
        results = []
        for idx in scores.argsort()[-top_k:][::-1]:
            results.append({
                'score': scores[idx],
                'document': self.documents[idx]
            })
        return results

if __name__ == "__main__":
    retriever = BM25Retriever('../data/knowledge_base.jsonl')
    query = "孔子认为什么是仁"
    results = retriever.retrieve(query, top_k=3)
    print(f"Query: {query}")
    print("Top results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. [{result['score']:.4f}] {result['document']['title']}: {result['document']['content']}")