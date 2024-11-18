import fitz  # PyMuPDF
import os
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def pdf_to_images():
    # スクリプトがあるディレクトリのパスを取得
    if hasattr(sys, '_MEIPASS'):
        # PyInstallerでパッケージ化された実行ファイルの場合
        script_dir = os.path.dirname(os.path.abspath(sys.executable))
        # 上位フォルダに保存
        output_base_dir = os.path.join(script_dir)
    else:
        # スクリプトとして実行される場合
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # スクリプトディレクトリに保存
        output_base_dir = script_dir
    
    print("スクリプトディレクトリ:", script_dir)
    print("出力ベースディレクトリ:", output_base_dir)
    
    # Tkinterのルートウィンドウを非表示にする
    Tk().withdraw()

    # PDFファイルを選択するためのファイルダイアログを開く
    pdf_path = askopenfilename(
        filetypes=[("PDFファイル", "*.pdf")],
        title="変換するPDFファイルを選択"
    )

    if not pdf_path:
        print("ファイルが選択されていません。")
        return

    # PDFファイルのベース名（拡張子なし）を抽出
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # 出力フォルダのパスを生成
    output_dir = os.path.join(output_base_dir, pdf_name)

    # 出力フォルダが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"ディレクトリを作成しました: {output_dir}")

    # PDFファイルを開く
    doc = fitz.open(pdf_path)

    # ページごとに繰り返し処理
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        
        # ズームレベルを設定（オプション）
        zoom = 1.0  # 必要に応じて調整
        mat = fitz.Matrix(zoom, zoom)
        
        # ページをピックスマップにレンダリング
        pix = page.get_pixmap(matrix=mat)

        # 出力画像のパスを定義
        image_path = os.path.join(output_dir, f"page_{page_num + 1}.jpg")

        # 画像をJPGとして保存
        pix.save(image_path)
        print(f"{image_path} を保存しました")

    # PDFを閉じる
    doc.close()
    print(f"\n変換が完了しました! 画像は以下に保存されています: {output_dir}")

    # キー入力を待機して終了
    # input("\n終了するには任意のキーを押してください...")

if __name__ == "__main__":
    pdf_to_images()
