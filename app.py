from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from services.translator import TranslatorService
from config.database import get_db, close_db
import os
from werkzeug.utils import secure_filename
from services.file_processor import FileProcessor
import uuid
import urllib.parse

app = Flask(__name__)
translator_service = TranslatorService()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

file_processor = FileProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text', '')
    source_lang = request.form.get('source_lang', 'auto')
    target_lang = request.form.get('target_lang', 'zh')
    provider = request.form.get('provider', 'google')
    translated_text = translator_service.translate_text(text, source_lang, target_lang, provider)
    return jsonify({'translated_text': translated_text})

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        provider = request.form.get('provider')
        api_key = request.form.get('api_key')
        base_url = request.form.get('base_url')
        db = get_db()
        db.execute('INSERT INTO user_config (provider, api_key, base_url) VALUES (?, ?, ?)', (provider, api_key, base_url))
        db.commit()
        return redirect(url_for('config'))
    return render_template('config.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        provider = request.form.get('provider', 'google')
        source_lang = request.form.get('source_lang', 'auto')
        target_lang = request.form.get('target_lang', 'zh')
        if not file or not file.filename:
            return {'error': '未上传文件'}, 400
        # 兼容中文文件名
        raw_filename = file.filename
        filename = secure_filename(str(raw_filename))
        if not filename or filename == '':
            ext = os.path.splitext(raw_filename)[-1]
            filename = f"file_{uuid.uuid4().hex}{ext}"
        # 上传文件保存为 xxx_upload.后缀
        name, ext_with_dot = os.path.splitext(filename)
        upload_filename = f"{name}_upload{ext_with_dot}"
        upload_path = os.path.join(UPLOAD_FOLDER, upload_filename)
        file.save(upload_path)
        ext = filename.rsplit('.', 1)[-1].lower()
        # 文本提取
        if ext == 'pdf':
            return {'error': '暂不支持PDF翻译，如需支持请联系开发者'}, 400
        elif ext == 'docx':
            text = file_processor.extract_text_from_word(upload_path)
        elif ext == 'md':
            text = file_processor.extract_text_from_markdown(upload_path)
        else:
            return {'error': '仅支持pdf、docx、md文件类型'}, 400
        # 分段翻译（优化：按段落分段，跳过空段）
        translator = TranslatorService()
        # 优先按两个换行分段，否则按单换行
        if '\n\n' in text:
            segments = [seg.strip() for seg in text.split('\n\n') if seg.strip()]
        else:
            segments = [seg.strip() for seg in text.split('\n') if seg.strip()]
        if not segments:
            return {'error': 'PDF无可翻译文本或为图片型PDF'}, 400
        translated_segments = []
        for seg in segments:
            try:
                translated = translator.translate_text(seg, source_lang, target_lang, provider)
            except Exception as e:
                translated = f"[翻译失败]{str(e)}"
            translated_segments.append(translated)
        translated_text = '\n'.join(translated_segments)
        # 生成翻译后文件，文件名与原始文件一致
        out_filename = filename
        out_path = os.path.join(UPLOAD_FOLDER, out_filename)
        if ext == 'pdf':
            file_processor.save_text_to_pdf(translated_text, out_path)
        elif ext == 'docx':
            file_processor.save_text_to_word(translated_text, out_path)
        elif ext == 'md':
            file_processor.save_text_to_markdown(translated_text, out_path)
        # 返回安全名和原始名
        return {'download_url': f'/download/{urllib.parse.quote(out_filename)}?origin={urllib.parse.quote(raw_filename)}'}
    return render_template('upload.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    # 支持中文文件名下载
    from flask import request
    origin = request.args.get('origin', filename)
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True, download_name=origin)

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
