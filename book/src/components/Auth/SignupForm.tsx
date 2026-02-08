import React, { useState } from 'react';
import styles from './Auth.module.css';

interface SignupFormProps {
  onSuccess?: (token: string) => void;
}

export default function SignupForm({ onSuccess }: SignupFormProps) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    softwareLevel: 'intermediate',
    hardwareLevel: 'beginner',
    roboticsKnowledge: false,
    learningGoals: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          software_level: formData.softwareLevel,
          hardware_level: formData.hardwareLevel,
          robotics_knowledge: formData.roboticsKnowledge,
          learning_goals: formData.learningGoals
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Signup failed');
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
      <h2>Sign Up</h2>
      
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
          minLength={8}
        />
      </div>

      <div className={styles.formGroup}>
        <label>Confirm Password</label>
        <input
          type="password"
          value={formData.confirmPassword}
          onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
          required
        />
      </div>

      <div className={styles.formGroup}>
        <label>Software Experience Level</label>
        <select
          value={formData.softwareLevel}
          onChange={(e) => setFormData({...formData, softwareLevel: e.target.value})}
        >
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>

      <div className={styles.formGroup}>
        <label>Hardware Experience Level</label>
        <select
          value={formData.hardwareLevel}
          onChange={(e) => setFormData({...formData, hardwareLevel: e.target.value})}
        >
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>

      <div className={styles.formGroup}>
        <label className={styles.checkbox}>
          <input
            type="checkbox"
            checked={formData.roboticsKnowledge}
            onChange={(e) => setFormData({...formData, roboticsKnowledge: e.target.checked})}
          />
          I have prior robotics knowledge
        </label>
      </div>

      <div className={styles.formGroup}>
        <label>Learning Goals (Optional)</label>
        <textarea
          value={formData.learningGoals}
          onChange={(e) => setFormData({...formData, learningGoals: e.target.value})}
          placeholder="What do you want to achieve with this course?"
          rows={3}
        />
      </div>

      <button type="submit" disabled={loading} className={styles.submitButton}>
        {loading ? 'Creating Account...' : 'Sign Up'}
      </button>
    </form>
  );
}