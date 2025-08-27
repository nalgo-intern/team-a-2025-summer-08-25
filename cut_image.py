from typing import Optional, Tuple
from PIL import Image, ImageTk, PngImagePlugin
import tkinter as tk

def select_and_crop(pil_image: PngImagePlugin.PngImageFile) -> Optional[PngImagePlugin.PngImageFile]:
    """
    Show a window with the given PIL (PNG) image, let the user drag to select a rectangle,
    crop to that rectangle, and return the cropped image as a PIL PNG image.
    
    Controls:
      - 左ドラッグ: 選択範囲を描画
      - Shift + 左ドラッグ: 既存の矩形を移動（ドラッグ開始が矩形内のとき）
      - Enter / Space / ダブルクリック: 決定（トリミングして返す）
      - Esc / 右クリック: キャンセル（None を返す）
    
    The image is scaled to fit the screen if necessary. Cropping is performed in the
    original image coordinates with correct scaling compensation.
    """
    # --- Tkセットアップ ---
    root = tk.Tk()
    root.title("Select area to crop (Enter/Space to confirm, Esc to cancel)")
    root.attributes("-topmost", True)  # 前面に
    root.update_idletasks()

    # 画面サイズ取得（余白を取って90%以内に収める）
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    max_w = int(screen_w * 0.9)
    max_h = int(screen_h * 0.9)

    # --- 表示用に縮小（必要なら） ---
    img_w, img_h = pil_image.size
    scale = 1.0
    disp_w, disp_h = img_w, img_h
    if img_w > max_w or img_h > max_h:
        scale = min(max_w / img_w, max_h / img_h)
        disp_w = int(img_w * scale)
        disp_h = int(img_h * scale)

    disp_img = pil_image if scale == 1.0 else pil_image.resize((disp_w, disp_h), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(disp_img)

    # --- キャンバス作成 ---
    canvas = tk.Canvas(root, width=disp_w, height=disp_h, highlightthickness=0, cursor="tcross")
    canvas.pack()
    canvas_img_id = canvas.create_image(0, 0, anchor="nw", image=tk_img)

    # 選択用状態
    rect_id = None
    start_xy: Tuple[int, int] = (0, 0)
    rect_bbox = [0, 0, 0, 0]  # x1, y1, x2, y2（表示座標系）
    moving = False  # 矩形移動モード
    move_anchor: Tuple[int, int] = (0, 0)

    # 完了フラグ
    result_img: Optional[Image.Image] = None
    done = tk.BooleanVar(value=False)

    def draw_or_update_rect(x1, y1, x2, y2):
        nonlocal rect_id, rect_bbox
        # 正規化
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        # 画像境界でクリップ
        x1 = max(0, min(disp_w, x1))
        x2 = max(0, min(disp_w, x2))
        y1 = max(0, min(disp_h, y1))
        y2 = max(0, min(disp_h, y2))
        rect_bbox = [x1, y1, x2, y2]
        if rect_id is None:
            rect_id = canvas.create_rectangle(x1, y1, x2, y2, outline="white", width=2)
            # 反転風の内側枠
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=1, dash=(3,2))
        else:
            # rect_id の次にある黒枠も更新
            canvas.coords(rect_id, x1, y1, x2, y2)
            # 次のアイテム（黒枠）を取得して座標更新
            next_id = rect_id + 1
            try:
                canvas.coords(next_id, x1, y1, x2, y2)
            except tk.TclError:
                pass

    def point_in_rect(x, y, bbox):
        x1, y1, x2, y2 = bbox
        return x1 <= x <= x2 and y1 <= y <= y2 and (x2 - x1) > 0 and (y2 - y1) > 0

    # --- マウスイベント ---
    def on_button_press(event):
        nonlocal start_xy, moving, move_anchor
        if event.num == 1:  # 左クリック
            if rect_id is not None and point_in_rect(event.x, event.y, rect_bbox) and event.state & 0x0001:
                # Shift 押しながら矩形内でドラッグ開始 => 移動モード
                moving = True
                move_anchor = (event.x, event.y)
            else:
                moving = False
                start_xy = (event.x, event.y)
                draw_or_update_rect(event.x, event.y, event.x, event.y)

    def on_mouse_move(event):
        nonlocal rect_bbox, move_anchor
        if rect_id is None:
            return
        if moving:
            dx = event.x - move_anchor[0]
            dy = event.y - move_anchor[1]
            move_anchor = (event.x, event.y)
            x1, y1, x2, y2 = rect_bbox
            w = x2 - x1
            h = y2 - y1
            nx1 = max(0, min(disp_w - w, x1 + dx))
            ny1 = max(0, min(disp_h - h, y1 + dy))
            draw_or_update_rect(nx1, ny1, nx1 + w, ny1 + h)
        else:
            if start_xy is not None:
                draw_or_update_rect(start_xy[0], start_xy[1], event.x, event.y)

    def on_button_release(event):
        nonlocal moving
        moving = False

    def on_double_click(event):
        confirm_and_finish()

    def on_right_click(event):
        cancel_and_finish()

    # --- キーイベント ---
    def on_key(event):
        if event.keysym in ("Return", "space"):
            confirm_and_finish()
        elif event.keysym == "Escape":
            cancel_and_finish()

    # --- 完了/キャンセル ---
    def confirm_and_finish():
        nonlocal result_img
        x1, y1, x2, y2 = rect_bbox
        if x2 - x1 <= 0 or y2 - y1 <= 0:
            # 無効な選択はそのままキャンセル扱い
            cancel_and_finish()
            return
        # 表示座標 -> 元画像座標へ逆変換
        inv = 1.0 / scale
        crop_box = (
            int(round(x1 * inv)),
            int(round(y1 * inv)),
            int(round(x2 * inv)),
            int(round(y2 * inv)),
        )
        # 境界クリップ（念のため）
        cx1 = max(0, min(img_w, crop_box[0]))
        cy1 = max(0, min(img_h, crop_box[1]))
        cx2 = max(0, min(img_w, crop_box[2]))
        cy2 = max(0, min(img_h, crop_box[3]))
        if cx2 - cx1 <= 0 or cy2 - cy1 <= 0:
            cancel_and_finish()
            return
        result_img = pil_image.crop((cx1, cy1, cx2, cy2))
        done.set(True)

    def cancel_and_finish():
        done.set(True)

    # バインド
    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_button_release)
    canvas.bind("<Double-Button-1>", on_double_click)
    canvas.bind("<Button-3>", on_right_click)
    root.bind("<Key>", on_key)

    # ウィンドウを画像サイズに
    root.geometry(f"{disp_w}x{disp_h}+{int((screen_w-disp_w)/2)}+{int((screen_h-disp_h)/2)}")

    # モーダルっぽく
    root.grab_set()
    root.focus_force()

    # 完了までブロック
    root.wait_variable(done)
    try:
        root.destroy()
    except tk.TclError:
        pass

    # Pillow は PNG 形式の情報（テキストチャンク等）も持てますが、
    # ここでは単純に画像オブジェクトを返します（呼び出し側で .save(..., format="PNG") 可能）
    return result_img  # キャンセル時は None
