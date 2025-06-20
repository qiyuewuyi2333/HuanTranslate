from docx import Document
from fpdf import FPDF

class FileProcessor:
    def extract_text_from_pdf(self, file_path: str) -> str:
        # 伪代码，实际应调用pdfplumber等
        return "PDF文本内容"

    def extract_text_from_word(self, file_path: str) -> str:
        # 伪代码，实际应调用python-docx等
        return "Word文本内容"

    def extract_text_from_markdown(self, file_path: str) -> str:
        # 伪代码，实际应解析Markdown
        return "Markdown文本内容"

    def save_text_to_word(self, text: str, out_path: str):
        doc = Document()
        for para in text.split('\n'):
            doc.add_paragraph(para)
        doc.save(out_path)

    def save_text_to_pdf(self, text: str, out_path: str):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(out_path)

    def save_text_to_markdown(self, text: str, out_path: str):
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)
