from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# テキスト分析API
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    input_text = data['text']

    # --- 感情分析処理 ---

    dummy_scores = {
        "入力された文章": input_text,
        "喜び": 3, "悲しみ": 0, "怒り": 1, "驚き": 2,
        "恐怖": 0, "嫌悪": 0, "信頼": 2, "期待": 1
    }
    return jsonify(dummy_scores)

# 画像分析API
@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    # 'image_file'というキーでファイルが送られてきたかチェック
    if 'image_file' not in request.files:
        return jsonify({"error": "画像ファイルがありません"}), 400

    file = request.files['image_file']

    # ファイル名が空でないかチェック
    if file.filename == '':
        return jsonify({"error": "ファイルが選択されていません"}), 400

    # --- OCR処理 ---

    # ダミーのテキストを返す
    extracted_text = "画像から抽出したテキストです。今日は良い天気ですね。"

    # --- 感情分析処理 ---

    dummy_scores = {
        "入力された文章": extracted_text,
        "喜び": 3,
        "悲しみ": 0,
        "怒り": 0,
        "驚き": 1,
        "恐怖": 0,
        "嫌悪": 0,
        "信頼": 3,
        "期待": 2
    }
    return jsonify(dummy_scores)


if __name__ == '__main__':
    app.run(debug=True)