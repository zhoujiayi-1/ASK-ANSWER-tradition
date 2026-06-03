import re

class SimpleReader:
    def __init__(self):
        pass
    
    def extract_answer(self, question, context):
        if not context or not question:
            return None, 0.0
        
        patterns = [
            r'曰[:：]\s*([^。？！；；]+)',
            r'道[:：]\s*([^。？！；；]+)',
            r'以为[:：]\s*([^。？！；；]+)',
            r'是谓[:：]\s*([^。？！；；]+)',
            r'所谓[:：]\s*([^。？！；；]+)',
            r'言[:：]\s*([^。？！；；]+)',
            r'云[:：]\s*([^。？！；；]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, context)
            if match:
                answer = match.group(1).strip()
                if len(answer) > 0 and len(answer) < 50:
                    return answer, 0.8
        
        keywords = ['仁', '道', '德', '义', '礼', '智', '信']
        for keyword in keywords:
            if keyword in question:
                idx = context.find(keyword)
                if idx != -1:
                    start = max(0, idx - 5)
                    end = min(len(context), idx + 15)
                    snippet = context[start:end]
                    return snippet.strip(), 0.6
        
        sentences = re.split(r'[。？！；；]', context)
        for sentence in sentences:
            if len(sentence) > 0 and len(sentence) < 40:
                has_keyword = any(k in sentence for k in ['曰', '道', '言', '谓'])
                if has_keyword or len(sentence) < 15:
                    return sentence.strip(), 0.5
        
        return None, 0.0

class Reader:
    def __init__(self, model_name=None, device=-1):
        self.reader = SimpleReader()
    
    def extract_answer(self, question, context):
        return self.reader.extract_answer(question, context)

if __name__ == "__main__":
    reader = Reader()
    question = "孔子认为什么是仁"
    context = "樊迟问仁。子曰：爱人。问知。子曰：知人。"
    answer, score = reader.extract_answer(question, context)
    print(f"Question: {question}")
    print(f"Context: {context}")
    print(f"Answer: {answer} (Score: {score:.4f})")