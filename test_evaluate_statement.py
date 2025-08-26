# pip install -q transformers fugashi unidic_lite accelerate
import evaluate_statement as es

es.get_runtime()

result = es.analyze_text("今日は最高の気分！")
print(result)

while True:
    text = input("テキストを入力してください（終了するには 'exit' と入力）：")
    if text.lower() == 'exit':
        break
    result = es.analyze_text(text)
    es.pretty_print(result)