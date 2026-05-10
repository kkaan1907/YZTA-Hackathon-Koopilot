import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==================== AI / Mesaj Analiz ====================

/**
 * Müşteri mesajını AI ile analiz eder.
 * @param {string} message - Müşteri mesajı
 * @param {string|null} sessionId - Oturum kimliği (sohbet hafızası için)
 * @returns {Promise} AI analiz sonucu + oluşturulan sipariş + kargo bilgisi
 */
export const analyzeMessage = async (message, sessionId = null) => {
  const response = await api.post('/ai/analyze-message', {
    message,
    session_id: sessionId,
  });
  return response.data;
};

// ==================== Stok / Envanter ====================

/**
 * Tüm ürünleri ve stok durumlarını getirir.
 * @returns {Promise} Ürün listesi
 */
export const getInventory = async () => {
  const response = await api.get('/inventory');
  return response.data;
};

/**
 * Ürün stok günceller.
 * @param {number} productId - Ürün ID
 * @param {number} stock - Yeni stok miktarı
 * @returns {Promise} Güncellenmiş ürün
 */
export const updateInventory = async (productId, stock) => {
  const response = await api.put(`/inventory/${productId}`, null, {
    params: { stock },
  });
  return response.data;
};

// ==================== Siparişler ====================

/**
 * Tüm siparişleri getirir.
 * @returns {Promise} Sipariş listesi
 */
export const getOrders = async () => {
  const response = await api.get('/orders');
  return response.data;
};

/**
 * Siparişi onaylar ve stoktan düşer.
 * @param {number} orderId - Sipariş ID
 * @returns {Promise} Onaylanmış sipariş
 */
export const approveOrder = async (orderId) => {
  const response = await api.put(`/orders/${orderId}/approve`);
  return response.data;
};

// ==================== Kargo ====================

/**
 * Mock kargo durumunu sorgular.
 * @param {number} orderId - Sipariş ID
 * @returns {Promise} Kargo durumu
 */
export const getShippingStatus = async (orderId) => {
  const response = await api.get(`/shipping/status/${orderId}`);
  return response.data;
};

// ==================== Günlük Özet ====================

/**
 * AI günlük özet raporu.
 * @returns {Promise} Günlük özet verisi
 */
export const getDailySummary = async () => {
  const response = await api.get('/ai/daily-summary');
  return response.data;
};

export default api;
