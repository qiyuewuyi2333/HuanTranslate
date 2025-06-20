from flask import Blueprint, request, jsonify

bp = Blueprint('translation', __name__)

@bp.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json() or {}
    text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    # 这里只做示例，实际应调用LLM客户端
    translated = f"[翻译]{text}"
    return jsonify({'translated_text': translated})
