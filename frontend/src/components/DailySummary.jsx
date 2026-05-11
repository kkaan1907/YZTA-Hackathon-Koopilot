import React, { useState, useEffect } from 'react';
import { getDailySummary } from '../services/api';
import { BarChart3, MessageSquare, AlertCircle, Calendar } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const DailySummary = () => {
  const [summary, setSummary] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const data = await getDailySummary();
        setSummary(data);
      } catch (error) {
        console.error('Özet verisi çekilemedi:', error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchSummary();
  }, []);
  if (isLoading) return <div style={{ padding: '24px' }}>Yükleniyor...</div>;
  if (!summary) return <div style={{ padding: '24px' }}>Veri bulunamadı.</div>;
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="glass-card" style={{
        padding: '32px',
        borderRadius: '24px',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ position: 'relative', zIndex: 1 }}>
          <h2 style={{ color: 'inherit', fontSize: '28px', marginBottom: '8px' }}>Günün Özeti 🌿</h2>
          <p style={{ opacity: 0.8, fontSize: '16px' }}>{summary.summary_text}</p>
        </div>
        <BarChart3 size={120} style={{
          position: 'absolute',
          right: '-20px',
          bottom: '-20px',
          opacity: 0.1,
          color: 'inherit'
        }} />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
        <div className="glass-card" style={{
          backgroundColor: 'var(--white)',
          padding: '24px',
          borderRadius: '20px',
          border: '1px solid var(--border-color)',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ color: 'var(--text-light)', fontSize: '14px' }}>Toplam Mesaj</span>
            <div style={{ padding: '8px', backgroundColor: 'rgba(45, 106, 79, 0.1)', borderRadius: '10px', color: 'var(--primary-mid)' }}>
              <MessageSquare size={20} />
            </div>
          </div>
          <div style={{ fontSize: '32px', fontWeight: '700' }}>{summary.total_messages}</div>
        </div>
        <div className="glass-card" style={{
          backgroundColor: 'var(--white)',
          padding: '24px',
          borderRadius: '20px',
          border: '1px solid var(--border-color)',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ color: 'var(--text-light)', fontSize: '14px' }}>Stok Uyarıları</span>
            <div style={{ padding: '8px', backgroundColor: 'rgba(230, 57, 70, 0.1)', borderRadius: '10px', color: 'var(--error)' }}>
              <AlertCircle size={20} />
            </div>
          </div>
          <div style={{ fontSize: '32px', fontWeight: '700' }}>{summary.low_stock_count}</div>
        </div>
      </div>
      <div className="glass-card" style={{
        backgroundColor: 'var(--white)',
        padding: '24px',
        borderRadius: '24px',
        border: '1px solid var(--border-color)'
      }}>
        <h3 style={{ marginBottom: '20px' }}>Niyet Dağılımı</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={Object.entries(summary.intent_distribution).map(([intent, count]) => ({
                    name: intent.replace('_', ' ').charAt(0).toUpperCase() + intent.replace('_', ' ').slice(1),
                    value: count
                  }))}
                  cx="50%"
                  cy="45%"
                  innerRadius={70}
                  outerRadius={100}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {Object.entries(summary.intent_distribution).map((entry, index) => {
                    const COLORS = ['#52B788', '#2D6A4F', '#74C69D', '#D6B98C', '#F4A261', '#2A9D8F'];
                    return <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />;
                  })}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--surface)', borderColor: 'var(--border-color)', borderRadius: '12px', color: 'var(--text-dark)', boxShadow: 'var(--shadow-soft)' }}
                  itemStyle={{ color: 'var(--primary-mid)', fontWeight: 'bold' }}
                />
                <Legend verticalAlign="bottom" height={36} iconType="circle" />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart 
                data={Object.entries(summary.intent_distribution).map(([intent, count]) => ({
                  name: intent.replace('_', ' ').charAt(0).toUpperCase() + intent.replace('_', ' ').slice(1),
                  Adet: count
                }))} 
                margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" vertical={false} />
                <XAxis dataKey="name" stroke="var(--text-light)" tick={{ fill: 'var(--text-light)', fontSize: 12 }} />
                <YAxis stroke="var(--text-light)" tick={{ fill: 'var(--text-light)', fontSize: 12 }} allowDecimals={false} />
                <Tooltip 
                  cursor={{ fill: 'var(--surface-soft)' }}
                  contentStyle={{ backgroundColor: 'var(--surface)', borderColor: 'var(--border-color)', borderRadius: '12px', color: 'var(--text-dark)', boxShadow: 'var(--shadow-soft)' }}
                  itemStyle={{ color: 'var(--primary-mid)', fontWeight: 'bold' }}
                />
                <Bar dataKey="Adet" fill="var(--primary-light)" radius={[6, 6, 0, 0]} barSize={40}>
                  {Object.entries(summary.intent_distribution).map((entry, index) => {
                    const COLORS = ['#52B788', '#2D6A4F', '#74C69D', '#D6B98C', '#F4A261', '#2A9D8F'];
                    return <Cell key={`bar-cell-${index}`} fill={COLORS[index % COLORS.length]} />;
                  })}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
export default DailySummary;