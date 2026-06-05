"""Gemini AI 摘要服務(T028/T029)。

以標準函式庫呼叫 Gemini REST API,將美食筆記濃縮成繁體中文摘要。
依 CLAUDE.md 規範:僅實作「摘要生成」,不做推薦系統。
"""
import json
import urllib.error
import urllib.request

from django.conf import settings

# Gemini generateContent REST 端點(金鑰以查詢字串帶入)
_ENDPOINT = (
    'https://generativelanguage.googleapis.com/v1beta/models/'
    '{model}:generateContent?key={key}'
)

# 提示詞:要求輸出一段精簡的繁體中文摘要,點出推薦重點與適合情境
_PROMPT = (
    '你是美食筆記摘要助理。請把以下使用者的美食筆記,'
    '濃縮成一段約 30~50 字的繁體中文摘要,點出推薦重點與適合的用餐情境。'
    '語氣自然、不要條列、不要加標題,只輸出摘要本身。\n\n筆記:\n{note}'
)


class GeminiError(Exception):
    """呼叫 Gemini API 失敗時拋出,訊息可直接顯示給使用者。"""


def _extract_api_error(exc):
    """從 HTTPError 回應內容取出 Gemini 的錯誤說明(若有),方便排查。"""
    try:
        body = json.loads(exc.read().decode('utf-8'))
        message = body.get('error', {}).get('message')
        return f':{message}' if message else ''
    except Exception:
        return ''


def generate_summary(note):
    """呼叫 Gemini API,將美食筆記轉成繁體中文摘要並回傳字串。

    未設定金鑰、筆記為空或 API 呼叫/解析失敗時,皆拋出 GeminiError。
    """
    if not settings.GEMINI_API_KEY:
        raise GeminiError('尚未設定 Gemini API 金鑰')

    note = (note or '').strip()
    if not note:
        raise GeminiError('筆記內容為空,無法產生摘要')

    url = _ENDPOINT.format(model=settings.GEMINI_MODEL, key=settings.GEMINI_API_KEY)
    payload = {'contents': [{'parts': [{'text': _PROMPT.format(note=note)}]}]}
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        raise GeminiError(f'Gemini API 回應錯誤(HTTP {exc.code}){_extract_api_error(exc)}') from exc
    except urllib.error.URLError as exc:
        raise GeminiError('無法連線到 Gemini API,請稍後再試') from exc

    try:
        text = result['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError, TypeError) as exc:
        raise GeminiError('Gemini API 回應格式無法解析') from exc

    summary = text.strip()
    if not summary:
        raise GeminiError('Gemini 未回傳有效摘要')
    return summary
