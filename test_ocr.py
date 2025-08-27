import ocr
from PIL import Image
import numpy as np

# --- CLI ---
if __name__ == "__main__":
    import os

    # ========== 重い処理の事前実行 ==========
    lang = "japan"
    ocr_model = ocr._get_ocr(lang)                 # モデル読み込み（重い）
    run_ocr = ocr._make_runner(ocr_model)          # 実行関数確定（分岐を前倒し）

    try:
        dummy = np.zeros((1, 1, 3), dtype=np.uint8)  # 真っ黒 1x1
        _ = run_ocr(dummy)
    except Exception:
        # 環境によっては不要/失敗しても実使用に支障なし
        pass

    # ========== 画像処理ループ ==========
    while 1:
        try:
            img_path = input("画像ファイルのパスを入力してください（終了するには Ctrl+C）: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n終了します。")
            break

        if not os.path.isfile(img_path):
            print(f"ファイルが見つかりません: {img_path}")
            continue

        try:
            img = Image.open(str(img_path))
            print(f"画像の型: {type(img)}")
        except Exception as e:
            print(f"画像の読み込みに失敗しました: {e}")
            continue

        try:
            text = ocr.ocr_from_pil_png(img, run_ocr=run_ocr)# OCR 実行 ここのimgに<class 'PIL.PngImagePlugin.PngImageFile'>の画像を渡す
            print(text if text else "（テキストは検出されませんでした）")
        except Exception as e:
            print(f"OCR 中にエラーが発生しました: {e}")