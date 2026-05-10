import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import MessagePanel from './components/MessagePanel';
import OrderPanel from './components/OrderPanel';
import InventoryPanel from './components/InventoryPanel';
import ShippingPanel from './components/ShippingPanel';
import DailySummary from './components/DailySummary';
function App() {
  const [activeTab, setActiveTab] = useState('messages');
  const [searchTerm, setSearchTerm] = useState('');
  const [chatMessages, setChatMessages] = useState([
    { id: 1, type: 'ai', text: 'Merhaba! Ben Koopilot. Sipariş, stok veya kargo ile ilgili size nasıl yardımcı olabilirim? 🌿' }
  ]);
  const [chatLoading, setChatLoading] = useState(false);
  const [chatSessionId] = useState(`session_${Math.random().toString(36).substr(2, 9)}`);
  const renderContent = () => {
    switch (activeTab) {
      case 'messages':
        return (
          <MessagePanel
            messages={chatMessages}
            setMessages={setChatMessages}
            isLoading={chatLoading}
            setIsLoading={setChatLoading}
            sessionId={chatSessionId}
          />
        );
      case 'orders':
        return <OrderPanel />;
      case 'inventory':
        return <InventoryPanel searchTerm={searchTerm} />;
      case 'summary':
        return <DailySummary />;
      case 'shipping':
        return <ShippingPanel />;
      default:
        return (
          <MessagePanel
            messages={chatMessages}
            setMessages={setChatMessages}
            isLoading={chatLoading}
            setIsLoading={setChatLoading}
            sessionId={chatSessionId}
          />
        );
    }
  };
  const getTitle = () => {
    const titles = {
      messages: 'Mesaj Analizi & AI Ajan',
      orders: 'Sipariş Yönetimi',
      inventory: 'Stok ve Envanter',
      shipping: 'Kargo Takibi',
      summary: 'Günlük Operasyon Özeti'
    };
    return titles[activeTab] || 'Dashboard';
  };
  return (
    <div className="dashboard-layout">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="main-container">
        <Header 
          title={getTitle()} 
          searchTerm={searchTerm} 
          setSearchTerm={setSearchTerm} 
        />
        <main className="content-area">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}
export default App;
