# pip install -q transformers fugashi unidic_lite accelerate
import evaluate_statement as es

def pct(p: float) -> str:
    return f"{p*100:.1f}%"

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

es.get_runtime()

result = es.analyze_text("今日は最高の気分！")
print(result)
pretty_print(result)

while True:
    text = input("テキストを入力してください（終了するには 'exit' と入力）：")
    if text.lower() == 'exit':
        break
    result = es.analyze_text(text)
    pretty_print(result)