from fugashi import Tagger
from typing import Dict
import os

def wakati_text(text: str):
    tagger = Tagger()
    return [word.surface for word in tagger(text)]

def load_wago_dict(filepath):
    """
    和語感情極性辞書を読み込み、単語→スコアの辞書を返す
    ネガ（経験）/ネガ（評価）: -1, ポジ（経験）/ポジ（評価）: +1
    """
    word_score = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "\t" not in line:
                continue
            label, word = line.split("\t", 1)
            if label.startswith("ネガ"):
                score = -1
            elif label.startswith("ポジ"):
                score = 1
            else:
                score = 0
            word_score[word.strip()] = score
    return word_score

def load_pn_dict(filepath):
    """
    日本語評価極性辞書（pn.csv.m3.120408.trim）を読み込み
    フォーマット: 表層形,よみ,品詞,極性値
    極性値: -1, 1, 0
    "２，３日"	e	〜である・になる（状態）客観
    """
    word_score = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            #スペース区切りをリストに変換
            parts = line.strip().split(" ")
            word, label, _ = line.split("\t", 2)
            if label == "p":
                score = 1
            elif label == "n":
                score = -1
            else:
                score = 0
            word_score[word.strip()] = score
    return word_score

def analyze_words(text):
    """
    テキストから単語を抽出し、各単語にスコアを付与した辞書のリストを返す
    """
    # 和語感情極性辞書のパス
    dict_path_wago = os.path.join(os.path.dirname(__file__), "wago.121808.pn")
    dict_path_pn = os.path.join(os.path.dirname(__file__), "pn.csv.m3.120408.trim")

    word_score = {}
    # 両方の辞書をマージ
    word_score.update(load_wago_dict(dict_path_wago))
    word_score.update(load_pn_dict(dict_path_pn))

    words = wakati_text(text)
    result = []
    for w in words:
        score = word_score.get(w, 0)
        result.append({w: score})
    return result

def negaposi_text(dict_list):
    negaposi = []
    for item in dict_list:
        for word, score in item.items():
            if score > 0:
                negaposi.append(f'<span class="positive">{word}</span>')
            elif score < 0:
                negaposi.append(f'<span class="negative">{word}</span>')
            else:
                negaposi.append(word)
    return " ".join(negaposi)

def span_text(text: str) -> str:
    dict_list = analyze_words(text)
    return negaposi_text(dict_list)

# if __name__ == "__main__":
#     text = "私はチャンスを掴んだ"
#     result = span_text(text)
#     print(result)
