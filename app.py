from flask import Flask, request, jsonify, render_template
import evaluate_statement as es
from PIL import Image

es.get_runtime()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# テキスト分析API
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    input_text = data['text']

    model_result = es.analyze_text(input_text)
    
    return jsonify(model_result)

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
    
    input_image = Image.open(file.stream)
    
    # --- OCR処理 ---
    # OCR(input_image) -> extracted_text

    # ダミーのテキストを返す
    extracted_text = "画像から抽出したテキストです。今日は良い天気ですね。"

    model_result = es.analyze_text(extracted_text)
    
    return jsonify(model_result)


if __name__ == '__main__':
    app.run(debug=True)