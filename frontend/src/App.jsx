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
  const renderContent = () => {
    switch (activeTab) {
      case 'messages':
        return <MessagePanel />;
      case 'orders':
        return <OrderPanel />;
      case 'inventory':
        return <InventoryPanel searchTerm={searchTerm} />;
      case 'summary':
        return <DailySummary />;
      case 'shipping':
        return <ShippingPanel />;
      default:
        return <MessagePanel />;
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