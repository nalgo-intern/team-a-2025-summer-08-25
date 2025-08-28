POLARITY_MAP = {
    'negative': {'ja': 'ネガティブ', 'icon': '&#x1f621;'},
    'neutral': {'ja': '普通', 'icon': '&#x1f610;'},
    'positive': {'ja': 'ポジティブ', 'icon': '&#x1f60a;'}
}

EMOTION_MAP = {
    'joy': {'ja': '喜び', 'icon': '&#x1f60a;'},
    'anticipation': {'ja': '期待', 'icon': '&#x1f929;'},
    'surprise': {'ja': '驚き', 'icon': '&#x1f62f;'},
    'trust': {'ja': '信頼', 'icon': '&#x1f60c;'},
    'disgust': {'ja': '嫌悪', 'icon': '&#x1f47f;'},
    'sadness': {'ja': '悲しみ', 'icon': '&#x1f972;'},
    'anger': {'ja': '怒り', 'icon': '&#x1f620;'},
    'fear': {'ja': '恐れ', 'icon': '&#x1f628;'}
}

def add_emotion_information(data):
    if 'polarity' in data and 'pred' in data.get('polarity', {}):
        label = data['polarity']['pred'].get('label') 
        
        # 英語ラベルがマッピング辞書に存在する場合
        if label in POLARITY_MAP:
            data['polarity']['pred']['ja'] = POLARITY_MAP[label]['ja']
            data['polarity']['pred']['icon'] = POLARITY_MAP[label]['icon']
            
    if 'polarity' in data and 'detail' in data.get('polarity', {}):
        # 各極性データ（辞書）をループ処理
        for polarity_data in data['polarity']['detail']:
            label = polarity_data.get('label') 
            
            # 英語ラベルがマッピング辞書に存在する場合
            if label in POLARITY_MAP:
                polarity_data['ja'] = POLARITY_MAP[label]['ja']
                polarity_data['icon'] = POLARITY_MAP[label]['icon']
    
    if 'emotion' in data and 'detail' in data.get('emotion', {}):
        # 各感情データ（辞書）をループ処理
        for emotion_data in data['emotion']['detail']:
            label = emotion_data.get('label') 
            
            # 英語ラベルがマッピング辞書に存在する場合
            if label in EMOTION_MAP:
                emotion_data['ja'] = EMOTION_MAP[label]['ja']
                emotion_data['icon'] = EMOTION_MAP[label]['icon']
                
    return data

def extract_emotion(data, threshold=0.1):
    if 'emotion' in data and 'detail' in data.get('emotion', {}):
        # 'prob'の値がしきい値より大きい要素だけをリストに含める
        filtered_details = [
            emotion_data for emotion_data in data['emotion']['detail']
            if emotion_data.get('prob', 0) > threshold
        ]
        # 抽出したリストで置き換え
        data['emotion']['repre'] = filtered_details

    return data