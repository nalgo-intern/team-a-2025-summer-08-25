from functools import lru_cache
from typing import List, Union, Callable, Tuple
from PIL.PngImagePlugin import PngImageFile
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR
import logging

logging.getLogger("ppocr").setLevel(logging.ERROR)

@lru_cache(maxsize=1)
def _get_ocr(lang: str = "japan") -> PaddleOCR:
    """
    PaddleOCR 3.x: predict() を使う前提。
    旧版でも angle_cls 付き ocr() にフォールバック。
    """
    try:
        # 不要なら前処理をオフにして軽量化
        return PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            lang=lang
        )
    except TypeError:
        # 2.x 系など
        return PaddleOCR(use_angle_cls=True, lang=lang)

def _extract_texts(result) -> List[str]:
    """
    PaddleOCR 3.x の predict() 形式（res.rec_texts）と
    2.x の ocr() 形式（[[box, (text, score)], ...]）の両対応。
    """
    texts: List[str] = []
    if not result:
        return texts

    # --- 3.x 系: list[PredictorResult] または list[dict] ---
    def try_new_pipeline():
        nonlocal texts
        for r in result if isinstance(result, list) else [result]:
            d = getattr(r, "res", r)  # PredictorResult.res または dict を想定
            if isinstance(d, dict):
                core = d.get("res", d)
                # 代表的フォーマット: {'res': {..., 'rec_texts': [...], ...}}
                if isinstance(core, dict) and "rec_texts" in core:
                    texts.extend([t for t in core["rec_texts"] if isinstance(t, str)])
                # 別系: {'res': [{'text': '...'}, ...]}
                elif isinstance(core, dict) and isinstance(core.get("res"), list):
                    for item in core["res"]:
                        if isinstance(item, dict) and isinstance(item.get("text"), str):
                            texts.append(item["text"])
                # さらに素朴な: [{'text': '...'}, ...]
                elif isinstance(core, list):
                    for item in core:
                        if isinstance(item, dict) and isinstance(item.get("text"), str):
                            texts.append(item["text"])

    # --- 2.x 系: ocr() 形式 ---
    def try_old_pipeline():
        nonlocal texts
        if isinstance(result, list):
            for part in result:
                if isinstance(part, list):
                    for it in part:
                        if isinstance(it, (list, tuple)) and len(it) >= 2:
                            cand = it[1]
                            if isinstance(cand, (list, tuple)) and cand and isinstance(cand[0], str):
                                texts.append(cand[0])

    try_new_pipeline()
    if not texts:
        try_old_pipeline()
    return texts

def _make_runner(ocr: PaddleOCR) -> Callable[[np.ndarray], List[str]]:
    """
    3.x/2.x を判別して、画像(BGR np.ndarray)→texts の実行関数を返す。
    """
    # 3.x 系
    if hasattr(ocr, "predict"):
        def _run(bgr: np.ndarray) -> List[str]:
            result = ocr.predict(bgr)
            return _extract_texts(result)
        return _run

    # 2.x 系
    def _run(bgr: np.ndarray) -> List[str]:
        try:
            result = ocr.ocr(bgr, cls=True)
        except TypeError:
            result = ocr.ocr(bgr)
        return _extract_texts(result)

    return _run

def ocr_from_pil_png(
    img: Union[PngImageFile, Image.Image],
    run_ocr: Callable[[np.ndarray], List[str]]
) -> str:
    if not isinstance(img, Image.Image):
        raise TypeError("image must be a PIL image (PngImageFile)")

    # PIL -> numpy(BGR)
    rgb = img.convert("RGB")
    arr = np.array(rgb)
    bgr = arr[:, :, ::-1]

    texts = run_ocr(bgr)
    return "\n".join(t for t in texts if t).strip()