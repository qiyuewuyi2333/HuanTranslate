from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from services.translator import TranslatorService
from config.database import get_db, close_db
import os
from werkzeug.utils import secure_filename
from services.file_processor import FileProcessor

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
        filename = secure_filename(str(file.filename))
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        ext = filename.rsplit('.', 1)[-1].lower()
        # 文本提取
        if ext == 'pdf':
            text = file_processor.extract_text_from_pdf(file_path)
        elif ext == 'docx':
            text = file_processor.extract_text_from_word(file_path)
        elif ext == 'md':
            text = file_processor.extract_text_from_markdown(file_path)
        else:
            return {'error': '暂不支持的文件类型'}, 400
        # 分段翻译
        translator = TranslatorService()
        segments = translator.split_long_text(text, 2000)
        translated_segments = []
        for seg in segments:
            translated = translator.translate_text(seg, source_lang, target_lang, provider)
            translated_segments.append(translated)
        translated_text = '\n'.join(translated_segments)
        # 生成翻译后文件
        out_filename = filename
        
        out_path = os.path.join(UPLOAD_FOLDER, out_filename)
        if ext == 'pdf':
            file_processor.save_text_to_pdf(translated_text, out_path)
        elif ext == 'docx':
            file_processor.save_text_to_word(translated_text, out_path)
        elif ext == 'md':
            file_processor.save_text_to_markdown(translated_text, out_path)
        return {'download_url': f'/download/{out_filename}'}
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
