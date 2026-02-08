import React, { useState } from 'react';
import styles from './Auth.module.css';

interface SigninFormProps {
  onSuccess?: (token: string) => void;
}

export default function SigninForm({ onSuccess }: SigninFormProps) {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Sign in failed');
      }

      const data = await response.json();
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user_id', data.user_id);
      
      if (onSuccess) {
        onSuccess(data.access_token);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <h2>Sign In</h2>
      
      {error && <div className={styles.error}>{error}</div>}

      <div className={styles.formGroup}>
        <label>Email</label>
        <input
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
          required
        />
      </div>

      <div className={styles.formGroup}>
        <label>Password</label>
        <input
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({...formData, password: e.target.value})}
          required
        />
      </div>

      <button type="submit" disabled={loading} className={styles.submitButton}>
        {loading ? 'Signing In...' : 'Sign In'}
      </button>
    </form>
  );
}