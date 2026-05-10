import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, AlertCircle, ShoppingBag } from 'lucide-react';
import { analyzeMessage } from '../services/api';
const MessagePanel = ({ messages, setMessages, isLoading, setIsLoading, sessionId }) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);
  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    const userMsg = { id: Date.now(), type: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);
    try {
      const data = await analyzeMessage(input, sessionId);
      const aiMsg = { 
        id: Date.now() + 1, 
        type: 'ai', 
        text: data.ai_analysis.ai_reply_draft,
        orderData: data.created_order,
        warnings: data.warnings
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        id: Date.now() + 1, 
        type: 'ai', 
        text: 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.', 
        isError: true 
      }]);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      backgroundColor: 'var(--white)',
      borderRadius: '24px',
      boxShadow: '0 4px 20px rgba(0,0,0,0.05)',
      overflow: 'hidden'
    }}>
      {}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '24px',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px'
      }}>
        {messages.map((msg) => (
          <div key={msg.id} style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: msg.type === 'user' ? 'flex-end' : 'flex-start',
            gap: '8px'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              flexDirection: msg.type === 'user' ? 'row-reverse' : 'row'
            }}>
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                backgroundColor: msg.type === 'user' ? 'var(--accent-earth)' : 'var(--primary-light)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: msg.type === 'user' ? 'var(--white)' : 'var(--primary-dark)'
              }}>
                {msg.type === 'user' ? <User size={16} /> : <Bot size={18} />}
              </div>
              <span style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-light)' }}>
                {msg.type === 'user' ? 'Müşteri' : 'Koopilot'}
              </span>
            </div>
            <div style={{
              maxWidth: '80%',
              padding: '16px',
              borderRadius: msg.type === 'user' ? '20px 20px 4px 20px' : '20px 20px 20px 4px',
              backgroundColor: msg.type === 'user' ? 'var(--primary-dark)' : '#F3F4F6',
              color: msg.type === 'user' ? 'var(--white)' : 'var(--text-dark)',
              fontSize: '15px',
              lineHeight: '1.6',
              whiteSpace: 'pre-wrap'
            }}>
              {msg.text}
              {}
              {msg.warnings && msg.warnings.length > 0 && (
                <div style={{
                  marginTop: '12px',
                  padding: '10px',
                  backgroundColor: 'rgba(230, 57, 70, 0.1)',
                  borderRadius: '8px',
                  display: 'flex',
                  gap: '8px',
                  color: 'var(--error)',
                  fontSize: '13px'
                }}>
                  <AlertCircle size={16} />
                  <div>{msg.warnings.join(', ')}</div>
                </div>
              )}
              {}
              {msg.orderData && (
                <div style={{
                  marginTop: '12px',
                  padding: '12px',
                  backgroundColor: 'var(--white)',
                  borderRadius: '12px',
                  border: '1px solid var(--border-color)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <ShoppingBag size={18} color="var(--success)" />
                    <div>
                      <div style={{ fontWeight: '600', color: 'var(--text-dark)' }}>Sipariş Taslağı Oluşturuldu</div>
                      <div style={{ fontSize: '12px', color: 'var(--text-light)' }}>ID: #{msg.orderData.order_id}</div>
                    </div>
                  </div>
                  <div style={{
                    padding: '4px 8px',
                    backgroundColor: 'rgba(42, 157, 143, 0.1)',
                    color: 'var(--success)',
                    fontSize: '12px',
                    fontWeight: '600',
                    borderRadius: '6px'
                  }}>
                    TASLAK
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center', color: 'var(--text-light)' }}>
            <Bot size={18} />
            <span style={{ fontSize: '14px', fontStyle: 'italic' }}>Koopilot düşünüyor...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      {}
      <form onSubmit={handleSend} style={{
        padding: '24px',
        borderTop: '1px solid var(--border-color)',
        display: 'flex',
        gap: '12px'
      }}>
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Müşteri mesajını buraya yazın..."
          style={{
            flex: 1,
            height: '48px',
            backgroundColor: '#F9FAFB',
            border: '1px solid var(--border-color)'
          }}
          disabled={isLoading}
        />
        <button 
          type="submit"
          disabled={isLoading || !input.trim()}
          style={{
            backgroundColor: 'var(--primary-mid)',
            color: 'var(--white)',
            width: '48px',
            height: '48px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            opacity: isLoading || !input.trim() ? 0.6 : 1
          }}
        >
          <Send size={20} />
        </button>
      </form>
    </div>
  );
};
export default MessagePanel;
