# pip install Flask
from flask import Flask, request, jsonify, render_template
import evaluate_statement as es

es.get_runtime()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # フロントエンドから送られてきたJSONデータを取得
    data = request.get_json()
    input_text = data['text']
    
    result = es.analyze_text(input_text)
    print(result)
    
    # 分析結果の取得（今回はダミーを使用）
    dummy_scores = {
        "入力された文章": input_text,
        "喜び": 3,
        "悲しみ": 0,
        "怒り": 1,
        "驚き": 2,
        "恐怖": 0,
        "嫌悪": 0,
        "信頼": 2,
        "期待": 1
    }

    # 結果をJSON形式でフロントエンドに返す
    return jsonify(dummy_scores)

if __name__ == '__main__':
    app.run(debug=True)