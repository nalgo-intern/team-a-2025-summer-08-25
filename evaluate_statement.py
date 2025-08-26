from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import torch
from transformers import pipeline, AutoConfig

# =========================
# ユーティリティ
# =========================
def degree_ja(p: float) -> str:
    if p >= 0.85: return "とても"
    if p >= 0.70: return "かなり"
    if p >= 0.55: return "やや"
    if p >= 0.40: return "弱め"
    return "ごく弱い"

def pct(p: float) -> str:
    return f"{p*100:.1f}%"

# =========================
# ランタイム本体（シングルトン）
# =========================
@dataclass
class _Models:
    clf_polarity: Any
    clf_emotion: Any
    labels_a: List[str]
    b_label2emo: Dict[str, str]

_RUNTIME: Optional["_SentimentRuntime"] = None  # シングルトン保持

class _SentimentRuntime:
    """
    ・初回生成時にモデルを読み込み
    ・以降は同インスタンスを使い回し（Colab セッションが続く限り常駐）
    ・関数ベースAPI: analyze_text(s), analyze_texts(list)
    """
    def __init__(self):
        model_a_id = "LoneWolfgang/bert-for-japanese-twitter-sentiment"
        model_b_id = "Mizuiro-sakura/luke-japanese-large-sentiment-analysis-wrime"

        # GPU/CPU 自動判定
        device = 0 if torch.cuda.is_available() else -1

        # パイプライン作成（return_all_scores=True を固定）
        clf_polarity = pipeline(
            "sentiment-analysis",
            model=model_a_id,
            tokenizer=model_a_id,
            device=device,
            return_all_scores=True,
            truncation=True,
        )
        clf_emotion = pipeline(
            "sentiment-analysis",
            model=model_b_id,
            tokenizer=model_b_id,
            device=device,
            return_all_scores=True,
            truncation=True,
        )

        # ラベル取得
        cfg_a = AutoConfig.from_pretrained(model_a_id)
        cfg_b = AutoConfig.from_pretrained(model_b_id)
        labels_a = [cfg_a.id2label[i] for i in sorted(cfg_a.id2label.keys())]  # ['negative','neutral','positive']

        # WRIME 8感情マッピング
        b_index2emo = {
            0: "joy",
            1: "sadness",
            2: "anticipation",
            3: "surprise",
            4: "anger",
            5: "fear",
            6: "disgust",
            7: "trust",
        }
        b_label2emo = {f"LABEL_{i}": emo for i, emo in b_index2emo.items()}

        self.models = _Models(
            clf_polarity=clf_polarity,
            clf_emotion=clf_emotion,
            labels_a=labels_a,
            b_label2emo=b_label2emo,
        )

    # --------- 公開メソッド（単文）---------
    def analyze_text(self, text: str) -> Dict[str, Any]:
        return self._analyze_one(text)

    # --------- 公開メソッド（バッチ）---------
    def analyze_texts(self, texts: List[str]) -> List[Dict[str, Any]]:
        return [self._analyze_one(t) for t in texts]

    # --------- 内部：1件処理 ---------
    def _analyze_one(self, text: str) -> Dict[str, Any]:
        m = self.models

        # --- 極性 ---
        pol_scores = m.clf_polarity(text)[0]  # list[{'label','score'}]
        pol_dict = {d["label"].lower(): float(d["score"]) for d in pol_scores}
        pol_list = [(lab, pol_dict.get(lab, 0.0)) for lab in m.labels_a]
        pol_label, pol_prob = max(pol_list, key=lambda x: x[1])

        # --- 感情 ---
        emo_scores = m.clf_emotion(text)[0]
        emo_list = []
        for d in emo_scores:
            lab = d["label"]
            emo = m.b_label2emo.get(lab, lab)
            prob = float(d["score"])
            emo_list.append((emo, prob))
        emo_list_sorted = sorted(emo_list, key=lambda x: x[1], reverse=True)

        return {
            "text": text,
            "polarity": {
                "detail": [{"label": lab, "prob": prob, "degree": degree_ja(prob)} for lab, prob in pol_list],
                "pred": {"label": pol_label, "prob": pol_prob, "degree": degree_ja(pol_prob)}
            },
            "emotion": {
                "detail": [{"label": lab, "prob": prob, "degree": degree_ja(prob)} for lab, prob in emo_list_sorted]
            }
        }

# ========== 外部公開：シングルトン取得 & 関数API ==========
def get_runtime() -> _SentimentRuntime:
    """最初の呼び出し時にモデルを読み込み、以降は常駐インスタンスを返す。"""
    global _RUNTIME
    if _RUNTIME is None:
        _RUNTIME = _SentimentRuntime()
    return _RUNTIME

def analyze_text(text: str) -> Dict[str, Any]:
    """アプリ側はこの関数を直接呼べばOK（モデルは常駐）。"""
    return get_runtime().analyze_text(text)

def analyze_texts(texts: List[str]) -> List[Dict[str, Any]]:
    """バッチ版。"""
    return get_runtime().analyze_texts(texts)

# （任意）整形表示
def pretty_print(result: dict):
    text = result["text"]
    pol_pred = result["polarity"]["pred"]
    pol_detail = result["polarity"]["detail"]
    emo_detail = result["emotion"]["detail"]

    print("▼ 入力文")
    print(text)
    print("\n▼ 極性（ネガ・ニュートラル・ポジ）")
    print(f"  予測: {pol_pred['label']} / 確率: {pct(pol_pred['prob'])} / 程度: {pol_pred['degree']}")
    print("  内訳:")
    for d in pol_detail:
        print(f"    - {d['label']:>8}: {pct(d['prob'])} ({d['degree']})")

    print("\n▼ 感情（8種類すべて）")
    for d in emo_detail:
        print(f"    - {d['label']:>12}: {pct(d['prob'])} ({d['degree']})")