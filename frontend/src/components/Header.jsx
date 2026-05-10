import React from 'react';
import { Bell, User, Search } from 'lucide-react';
const Header = ({ title, searchTerm, setSearchTerm }) => {
  return (
    <header style={{
      height: 'var(--header-height)',
      backgroundColor: 'var(--white)',
      borderBottom: '1px solid var(--border-color)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      zIndex: 10
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
        <h2 style={{ fontSize: '20px', margin: 0 }}>{title}</h2>
        <div style={{
          position: 'relative',
          display: 'flex',
          alignItems: 'center'
        }}>
          <Search size={18} style={{ position: 'absolute', left: '12px', color: 'var(--text-light)' }} />
          <input 
            type="text" 
            placeholder="Ara..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              paddingLeft: '38px',
              backgroundColor: '#F9FAFB',
              border: 'none',
              width: '300px'
            }}
          />
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <button style={{
          backgroundColor: '#F9FAFB',
          padding: '8px',
          color: 'var(--text-dark)',
          position: 'relative'
        }}>
          <Bell size={20} />
          <span style={{
            position: 'absolute',
            top: '6px',
            right: '6px',
            width: '8px',
            height: '8px',
            backgroundColor: 'var(--error)',
            borderRadius: '50%',
            border: '2px solid var(--white)'
          }}></span>
        </button>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          padding: '4px 4px 4px 12px',
          backgroundColor: '#F9FAFB',
          borderRadius: '30px',
          border: '1px solid var(--border-color)'
        }}>
          <span style={{ fontSize: '14px', fontWeight: '500' }}>Yönetici</span>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            backgroundColor: 'var(--primary-light)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--primary-dark)'
          }}>
            <User size={18} />
          </div>
        </div>
      </div>
    </header>
  );
};
export default Header;