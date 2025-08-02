import os
from flask import Flask, request, jsonify, send_from_directory, session
import logging
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

# .env dosyasını yükle
load_dotenv()

# Flask uygulamasını oluştur
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Session için gerekli

# Logging ayarla
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env dosyasından API değerini al
api_key = os.getenv("GROQ_API_KEY")

# Groq API URL'i
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Konuşma geçmişini tutmak için (memory - her kullanıcı için ayrı)
conversation_history = {}

def load_personality():
    """Kişilik dosyasını yükle"""
    try:
        with open('personality.txt', 'r', encoding='utf-8') as f:
            personality_text = f.read()
        
        # Yorumları ve boş satırları temizle
        lines = personality_text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    except FileNotFoundError:
        logger.warning("personality.txt dosyası bulunamadı, varsayılan kişilik kullanılıyor")
        return "Sen yardımcı bir AI asistanısın. Arkadaşça ve samimi bir şekilde Türkçe yanıtlar veriyorsun."

def get_user_id():
    """Basit bir kullanıcı ID sistemi (session tabanlı)"""

    # Telegram gibi dış sistemden gelen kimlik varsa onu kullan
    if request.is_json:
        body = request.get_json()
        q = body.get("question", "")
        if q.startswith("[user_") and "]" in q:
            return q.split("]")[0].strip("[]")  # [user_12345] → user_12345
            
    if 'user_id' not in session:
        session['user_id'] = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return session['user_id']

def add_to_history(user_id, role, content):
    """Konuşma geçmişine mesaj ekle"""
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    conversation_history[user_id].append({
        'role': role,
        'content': content,
        'timestamp': datetime.now().isoformat()
    })
    
    # Son 10 mesajı tut (5 soru + 5 cevap)
    if len(conversation_history[user_id]) > 10:
        conversation_history[user_id] = conversation_history[user_id][-10:]

def get_conversation_context(user_id):
    """Son 5 mesaj çiftini (soru-cevap) al"""
    if user_id not in conversation_history:
        return []
    
    history = conversation_history[user_id]
    return history[-8:]  # Son 8 mesaj (4 soru-cevap çifti)

def call_groq_api(question, user_id):
    """Groq API'ye istek gönder"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Kişilik özelliklerini yükle
    personality = load_personality()
    
    # Konuşma geçmişini al
    context_messages = get_conversation_context(user_id)
    
    # Mesajları hazırla
    messages = [
        {
            "role": "system",
            "content": f"""Sen bir AI asistanısın. İşte kişilik özelliklerin:

{personality}

Konuşma tarzın bu özelliklere uygun olmalı. Samimi, yardımsever ve Türkçe yanıtlar ver. 
Geçmiş konuşmaları hatırla ve tutarlı ol."""
        }
    ]
    
    # Geçmiş konuşmaları ekle
    for msg in context_messages:
        messages.append({
            "role": msg['role'],
            "content": msg['content']
        })
    
    # Mevcut soruyu ekle
    messages.append({
        "role": "user",
        "content": question
    })
    
    data = {
        "messages": messages,
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.8,  # Biraz daha yaratıcı olsun
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        
        # Konuşma geçmişine ekle
        add_to_history(user_id, "user", question)
        add_to_history(user_id, "assistant", answer)
        
        return answer
    except requests.exceptions.RequestException as e:
        logger.error(f"API isteği hatası: {str(e)}")
        raise Exception(f"API bağlantı hatası: {str(e)}")
    except KeyError as e:
        logger.error(f"API yanıt formatı hatası: {str(e)}")
        raise Exception("API yanıt formatı beklenen gibi değil")
    except Exception as e:
        logger.error(f"Genel hata: {str(e)}")
        raise

# Ana sayfa
@app.route('/')
def index():
    """Ana sayfayı serve et"""
    return send_from_directory('.', 'index.html')

# CSS dosyası
@app.route('/style.css')
def style():
    """CSS dosyasını serve et"""
    return send_from_directory('.', 'style.css')

# JavaScript dosyası
@app.route('/script.js')
def script():
    """JS dosyasını serve et"""
    return send_from_directory('.', 'script.js')

@app.route('/ask', methods=['POST'])
def ask_question():
    """Soru-cevap endpoint'i"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'success': False, 'error': 'Soru boş olamaz'})
        
        # Kullanıcı ID'sini al
        user_id = get_user_id()
        
        logger.info(f"Soru alındı ({user_id}): {question}")
        
        # Groq API'ye istek gönder
        answer = call_groq_api(question, user_id)
        logger.info(f"Cevap oluşturuldu ({user_id}): {len(answer)} karakter")
        
        return jsonify({
            'success': True,
            'answer': answer,
            'question': question,
            'conversation_count': len(conversation_history.get(user_id, []))
        })
        
    except Exception as e:
        logger.error(f"Hata oluştu: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Konuşma geçmişini temizle"""
    try:
        user_id = get_user_id()
        if user_id in conversation_history:
            del conversation_history[user_id]
        
        return jsonify({
            'success': True,
            'message': 'Konuşma geçmişi temizlendi'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/get-history', methods=['GET'])
def get_history():
    """Konuşma geçmişini getir"""
    try:
        user_id = get_user_id()
        history = conversation_history.get(user_id, [])
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/health')
def health_check():
    """Sistem durumu kontrolü"""
    try:
        # Geçici kullanıcı ID'si ile test
        temp_user_id = "health_check_user"
        test_answer = call_groq_api("Merhaba", temp_user_id)
        
        # Test verilerini temizle
        if temp_user_id in conversation_history:
            del conversation_history[temp_user_id]
        
        return jsonify({
            'status': 'healthy',
            'groq_api': 'connected',
            'message': 'Sistem çalışıyor',
            'personality_loaded': os.path.exists('personality.txt'),
            'total_conversations': len(conversation_history),
            'test_response': test_answer[:50] + "..." if len(test_answer) > 50 else test_answer
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'groq_api': 'disconnected',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # API anahtarı kontrolü
    if api_key == "gsk-YOUR_API_KEY_HERE" or not api_key:
        print("⚠️  UYARI: Lütfen API anahtarınızı ayarlayın!")
        print("📝 .env dosyasındaki GROQ_API_KEY değişkenine gerçek API anahtarınızı yazın")
        print("🔗 API anahtarını şuradan alabilirsiniz: https://console.groq.com/keys")
        print("")
        print("Alternatif olarak .env dosyası oluşturup şunu yazabilirsiniz:")
        print("GROQ_API_KEY=your_actual_api_key_here")
        print("")
        choice = input("Yine de devam etmek istiyor musunuz? (y/N): ")
        if choice.lower() != 'y':
            exit(1)
    
    print("🚀 AI Soru-Cevap sistemi başlatılıyor...")
    print("📱 Tarayıcınızda http://localhost:5000 adresine gidin")
    print("🔧 Sistem durumu: http://localhost:5000/health")
    
    # Flask uygulamasını başlat
    app.run(host='0.0.0.0', port=5000, debug=True)