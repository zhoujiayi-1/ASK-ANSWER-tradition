import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from src.qa_system import QASystem

app = Flask(__name__)
qa_system = QASystem('./data/knowledge_base.jsonl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': '请输入问题'})
    
    answer, doc, sources = qa_system.query(question, top_k=3)
    
    return jsonify({
        'question': question,
        'answer': answer,
        'source': doc['title'] if doc else None,
        'sources': sources
    })

@app.route('/api/statistics')
def statistics():
    stats = {
        'total_docs': 101,
        'categories': {
            '论语': 25,
            '道德经': 16,
            '诗经': 12,
            '楚辞': 7,
            '孟子': 10,
            '庄子': 8,
            '周易': 6,
            '尚书': 3,
            '荀子': 3,
            '礼记': 3,
            '左传': 2,
            '韩非子': 2,
            '三国志': 2,
            '春秋': 1,
            '国语': 1
        },
        'hot_questions': [
            '孔子认为什么是仁？',
            '上善若水出自哪里？',
            '学而不思则罔下一句是什么？',
            '北冥有鱼出自哪部著作？',
            '天行健下一句是什么？',
            '生于忧患死于安乐出自哪里？'
        ]
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
