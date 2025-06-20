class ImageProcessor:
    def ocr_image(self, image_path: str, lang: str = 'chi_sim') -> str:
        # 伪代码，实际应调用pytesseract等
        return "图片识别文字"

    def translate_image(self, image_path: str, source_lang: str, target_lang: str) -> str:
        # 伪代码，先OCR再翻译
        text = self.ocr_image(image_path, source_lang)
        return f"[图片翻译]{text}"
