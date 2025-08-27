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
    if 'emotion' in data and 'detail' in data.get('emotion', {}):
        # 各感情データ（辞書）をループ処理
        for emotion_data in data['emotion']['detail']:
            label = emotion_data.get('label') 
            
            # 英語ラベルがマッピング辞書に存在する場合
            if label in EMOTION_MAP:
                emotion_data['ja'] = EMOTION_MAP[label]['ja']
                emotion_data['icon'] = EMOTION_MAP[label]['icon']
                
    return data