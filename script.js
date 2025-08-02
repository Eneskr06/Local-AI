// Sayfa yüklendiğinde çalışacak kodlar
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('question-input');
    const charCount = document.getElementById('char-count');
    
    // Karakter sayacını güncelle
    input.addEventListener('input', function() {
        const count = this.value.length;
        charCount.textContent = count;
        
        if (count > 450) {
            charCount.style.color = '#dc3545';
        } else if (count > 400) {
            charCount.style.color = '#ffc107';
        } else {
            charCount.style.color = '#666';
        }
    });
    
    // Input'a focus ver
    input.focus();
});

async function askQuestion() {
    const input = document.getElementById('question-input');
    const question = input.value.trim();
    
    if (!question) {
        input.focus();
        return;
    }
    
    const chatContainer = document.getElementById('chat-container');
    const askBtn = document.getElementById('ask-btn');
    
    // Kullanıcı mesajını ekle
    addMessage(question, 'user');
    input.value = '';
    document.getElementById('char-count').textContent = '0';
    
    // Butonu devre dışı bırak
    askBtn.disabled = true;
    askBtn.innerHTML = '<span>Yükleniyor...</span>';
    
    // Yükleniyor mesajı ekle
    const loadingMsg = addMessage('AI düşünüyor...', 'ai', 'loading-msg', true);
    
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        
        // Yükleniyor mesajını kaldır
        loadingMsg.remove();
        
        if (data.success) {
            addMessage(data.answer, 'ai');
            updateConversationCount(data.conversation_count);
        } else {
            addMessage(`❌ Üzgünüm, bir hata oluştu: ${data.error}`, 'ai');
        }
    } catch (error) {
        loadingMsg.remove();
        addMessage('❌ Bağlantı hatası oluştu. Lütfen tekrar deneyin.', 'ai');
        console.error('Fetch error:', error);
    }
    
    // Butonu tekrar etkinleştir
    askBtn.disabled = false;
    askBtn.innerHTML = '<span>Gönder</span>';
    input.focus();
}

function addMessage(text, type, id = null, isLoading = false) {
    const chatContainer = document.getElementById('chat-container');
    
    // Mesaj container'ı oluştur
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    if (isLoading) {
        messageDiv.className += ' loading';
    }
    if (id) {
        messageDiv.id = id;
    }
    
    // Mesaj içeriği
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (type === 'user') {
        contentDiv.innerHTML = `<strong>Sen:</strong> ${escapeHtml(text)}`;
    } else {
        contentDiv.innerHTML = `<strong>AI:</strong> ${escapeHtml(text)}`;
    }
    
    // Zaman damgası
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = getCurrentTime();
    
    // Elementleri birleştir
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);
    chatContainer.appendChild(messageDiv);
    
    // Scroll'u en alta kaydır
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return messageDiv;
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('tr-TR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        askQuestion();
    }
}

async function clearHistory() {
    const clearBtn = document.getElementById('clear-btn');
    
    if (!confirm('Konuşma geçmişini silmek istediğinizden emin misiniz?')) {
        return;
    }
    
    clearBtn.disabled = true;
    clearBtn.textContent = '🔄 Temizleniyor...';
    
    try {
        const response = await fetch('/clear-history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Chat container'ı temizle
            const chatContainer = document.getElementById('chat-container');
            chatContainer.innerHTML = `
                <div class="message ai-message">
                    <div class="message-content">
                        <strong>AI:</strong> Konuşma geçmişi temizlendi! Yeniden tanışalım 😊
                    </div>
                    <div class="message-time">${getCurrentTime()}</div>
                </div>
            `;
            
            updateConversationCount(0);
        } else {
            alert('Geçmiş temizlenirken hata oluştu: ' + data.error);
        }
    } catch (error) {
        alert('Bağlantı hatası oluştu.');
        console.error('Clear history error:', error);
    }
    
    clearBtn.disabled = false;
    clearBtn.textContent = '🗑️ Geçmişi Temizle';
}

function updateConversationCount(count) {
    const countElement = document.getElementById('conversation-count');
    if (count === 0) {
        countElement.textContent = 'Henüz mesaj yok';
    } else if (count === 1) {
        countElement.textContent = '1 mesaj';
    } else {
        countElement.textContent = `${count} mesaj`;
    }
}

// Sayfa kapanırken uyarı (isteğe bağlı)
window.addEventListener('beforeunload', function(e) {
    const chatContainer = document.getElementById('chat-container');
    const messages = chatContainer.querySelectorAll('.message');
    
    if (messages.length > 1) { // İlk karşılama mesajından fazlası varsa
        e.preventDefault();
        e.returnValue = '';
    }
});