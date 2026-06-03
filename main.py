import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.qa_system import QASystem

def print_welcome():
    print("=" * 50)
    print("            中国古典文学问答系统 v1.0")
    print("=" * 50)
    print("知识库包含：论语、道德经、诗经、楚辞、孟子、庄子")
    print("输入 'exit' 或 'quit' 退出系统")
    print("-" * 50)

def print_answer(answer, doc, sources):
    if not answer:
        print("抱歉，未找到相关答案")
        return
    
    print(f"\n答案：{answer}")
    if doc:
        print(f"来源：{doc['title']}")
    
    print("\n检索到的相关知识：")
    for i, source in enumerate(sources, 1):
        print(f"\n{i}. {source['title']}")
        print(f"   内容：{source['content']}")
        if source['answer']:
            print(f"   抽取答案：{source['answer']} (置信度: {source['answer_score']:.2f})")

def main():
    print_welcome()
    
    try:
        print("正在加载知识库和模型...")
        qa_system = QASystem('./data/knowledge_base.jsonl')
        print("加载完成！")
        print("-" * 50)
    except Exception as e:
        print(f"初始化失败：{e}")
        return
    
    while True:
        try:
            question = input("\n请输入您的问题：").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit', '退出']:
                print("\n感谢使用，再见！")
                break
            
            print("正在检索...")
            answer, doc, sources = qa_system.query(question, top_k=3)
            print_answer(answer, doc, sources)
            
        except KeyboardInterrupt:
            print("\n感谢使用，再见！")
            break
        except Exception as e:
            print(f"发生错误：{e}")

if __name__ == "__main__":
    main()