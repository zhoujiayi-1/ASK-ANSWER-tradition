from src.retriever import BM25Retriever
from src.reader import Reader

class QASystem:
    def __init__(self, knowledge_base_path, model_name="bert-base-chinese", device=-1):
        self.retriever = BM25Retriever(knowledge_base_path)
        self.reader = Reader(model_name=model_name, device=device)
    
    def query(self, question, top_k=5):
        retrieved_docs = self.retriever.retrieve(question, top_k=top_k)
        if not retrieved_docs:
            return None, None, []
        
        best_answer = None
        best_score = 0.0
        best_doc = None
        sources = []
        
        for item in retrieved_docs:
            doc = item['document']
            context = doc['content']
            answer, score = self.reader.extract_answer(question, context)
            
            sources.append({
                'title': doc['title'],
                'content': context,
                'source': doc['source'],
                'retrieval_score': item['score'],
                'answer_score': score,
                'answer': answer
            })
            
            if score > best_score and answer:
                best_score = score
                best_answer = answer
                best_doc = doc
        
        return best_answer, best_doc, sources

if __name__ == "__main__":
    qa_system = QASystem('../data/knowledge_base.jsonl')
    question = "孔子认为什么是仁"
    answer, doc, sources = qa_system.query(question, top_k=3)
    
    print(f"Question: {question}")
    print(f"\nBest Answer: {answer}")
    if doc:
        print(f"Source: {doc['title']}")
    
    print("\nRetrieved Sources:")
    for i, source in enumerate(sources, 1):
        print(f"{i}. [{source['retrieval_score']:.4f}] {source['title']}")
        print(f"   Answer: {source['answer']} (Score: {source['answer_score']:.4f})")