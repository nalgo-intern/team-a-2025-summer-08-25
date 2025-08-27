from flask import Flask, request, jsonify, render_template
from PIL import Image

#import evaluate_statement as es
import  data_editor as de

#es.get_runtime()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# テキスト分析API
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    input_text = data['text']

    #model_result = es.analyze_text(input_text)
    model_result = {'text': 'おはようございます！', 'polarity': {'detail': [{'label': 'negative', 'prob': 0.09024933725595474, 'degree': 'ごく弱い'}, {'label': 'neutral', 'prob': 0.7958078980445862, 'degree': 'かなり'}, {'label': 'positive', 'prob': 0.11394275724887848, 'degree': 'ごく弱い'}], 'pred': {'label': 'neutral', 'prob': 0.7958078980445862, 'degree': 'かなり'}}, 'emotion': {'detail': [{'label': 'joy', 'prob': 0.9646738767623901, 'degree': 'とても'}, {'label': 'anticipation', 'prob': 0.022037865594029427, 'degree': 'ごく弱い'}, {'label': 'surprise', 'prob': 0.004827785771340132, 'degree': 'ごく弱い'}, {'label': 'trust', 'prob': 0.0030676661990582943, 'degree': 'ごく弱い'}, {'label': 'disgust', 'prob': 0.002798834117129445, 'degree': 'ごく弱い'}, {'label': 'sadness', 'prob': 0.0019518053159117699, 'degree': 'ごく弱い'}, {'label': 'anger', 'prob': 0.0018896141555160284, 'degree': 'ごく弱い'}, {'label': 'fear', 'prob': 0.0010431797709316015, 'degree': 'ごく弱い'}]}}
    updated_result = de.add_emotion_information(model_result)
    filtered_result = de.extract_emotion(updated_result)
    print(filtered_result)
    
    return jsonify(filtered_result)
    

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

    #model_result = es.analyze_text(extracted_text)
    model_result = {'text': 'おはようございます！', 'polarity': {'detail': [{'label': 'negative', 'prob': 0.09024933725595474, 'degree': 'ごく弱い'}, {'label': 'neutral', 'prob': 0.7958078980445862, 'degree': 'かなり'}, {'label': 'positive', 'prob': 0.11394275724887848, 'degree': 'ごく弱い'}], 'pred': {'label': 'neutral', 'prob': 0.7958078980445862, 'degree': 'かなり'}}, 'emotion': {'detail': [{'label': 'joy', 'prob': 0.9646738767623901, 'degree': 'とても'}, {'label': 'anticipation', 'prob': 0.022037865594029427, 'degree': 'ごく弱い'}, {'label': 'surprise', 'prob': 0.004827785771340132, 'degree': 'ごく弱い'}, {'label': 'trust', 'prob': 0.0030676661990582943, 'degree': 'ごく弱い'}, {'label': 'disgust', 'prob': 0.002798834117129445, 'degree': 'ごく弱い'}, {'label': 'sadness', 'prob': 0.0019518053159117699, 'degree': 'ごく弱い'}, {'label': 'anger', 'prob': 0.0018896141555160284, 'degree': 'ごく弱い'}, {'label': 'fear', 'prob': 0.0010431797709316015, 'degree': 'ごく弱い'}]}}
    updated_result = de.add_emotion_information(model_result)
    filtered_result = de.extract_emotion(updated_result)
    print(filtered_result)
    
    return jsonify(filtered_result)


if __name__ == '__main__':
    app.run(debug=True)