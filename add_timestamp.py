import io
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pathlib import Path

def add_timestamps_to_pdf(input_pdf_path, output_pdf_path, frame_interval_sec, fps, images_per_page=5):
    # 開始ページを指定して新しいPDFを作成
    output_pdf = PyPDF2.PdfWriter()
    input_pdf = PyPDF2.PdfReader(str(input_pdf_path))

    for page_num in range(len(input_pdf.pages)):
        packet = io.BytesIO()
        original_page = input_pdf.pages[page_num]
        width = float(original_page.mediabox.upper_right[0])
        height = float(original_page.mediabox.upper_right[1])
        
        can = canvas.Canvas(packet, pagesize=(width, height))
        can.setFillColorRGB(1, 1, 1)  # 白色
        can.setFont("Helvetica", 20)  # 大きなフォントサイズ
        
        timestamp = (page_num * frame_interval_sec) / fps
        
        for i in range(images_per_page):
            text = f'Time: {timestamp:.2f} sec'
            img_height = height / images_per_page
            y_position = height - (i * img_height) - 20  # 各画像の左上にタイムスタンプを配置
            can.drawString(10, y_position, text)
        
        can.save()
        
        packet.seek(0)
        new_pdf = PyPDF2.PdfReader(packet)
        page = input_pdf.pages[page_num]
        page.merge_page(new_pdf.pages[0])
        output_pdf.add_page(page)

    with open(output_pdf_path, 'wb') as f:
        output_pdf.write(f)


def main():
    input_pdf_path = Path.cwd() / 'Get_out_of_bed1.pdf'
    output_pdf_path = Path.cwd() / f'{input_pdf_path.stem}_timestamp.pdf'
    frame_interval_sec = 0.5
    fps = 1

    add_timestamps_to_pdf(input_pdf_path, output_pdf_path, frame_interval_sec, fps)

if __name__ == '__main__':
    main()
