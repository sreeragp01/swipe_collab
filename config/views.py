from functools import lru_cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from deep_translator import GoogleTranslator

@lru_cache(maxsize=1000)
def cached_translate(text: str, source: str, target: str) -> str:
    translator = GoogleTranslator(source=source, target=target)
    return translator.translate(text)

@api_view(['POST'])
@permission_classes([AllowAny])
def translate_view(request):
    text = request.data.get('text', '').strip()
    target_lang = request.data.get('target_lang', 'en').lower()
    source_lang = request.data.get('source_lang', 'auto').lower()

    if not text:
        return Response({'error': 'text is required'}, status=status.HTTP_400_BAD_REQUEST)

    if '-' in target_lang:
        target_lang = target_lang.split('-')[0]

    try:
        translated_text = cached_translate(text, source_lang, target_lang)
        return Response({
            'original': text,
            'translated': translated_text,
            'source_lang': source_lang,
            'target_lang': target_lang
        })
    except Exception as e:
        return Response({
            'original': text,
            'translated': text,
            'error': str(e)
        }, status=status.HTTP_200_OK)
