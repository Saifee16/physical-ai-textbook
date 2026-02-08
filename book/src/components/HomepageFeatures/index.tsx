import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  icon: string;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Comprehensive Curriculum',
    icon: '📚',
    description: (
      <>
        13 weeks of structured content covering everything from ROS 2 fundamentals
        to advanced humanoid robotics and conversational AI integration.
      </>
    ),
  },
  {
    title: 'AI-Powered Learning',
    icon: '🤖',
    description: (
      <>
        Built-in RAG chatbot that answers your questions using course content.
        Get instant help and explanations as you learn.
      </>
    ),
  },
  {
    title: 'Hands-On Projects',
    icon: '🛠️',
    description: (
      <>
        Practical code examples, simulations, and a capstone project where you
        build an autonomous humanoid robot from scratch.
      </>
    ),
  },
  {
    title: 'Industry Tools',
    icon: '⚙️',
    description: (
      <>
        Learn with professional tools: ROS 2, Gazebo, NVIDIA Isaac, Unity.
        Everything you need for real-world robotics development.
      </>
    ),
  },
  {
    title: 'Personalized Content',
    icon: '🎯',
    description: (
      <>
        Content adapts to your experience level. Whether you're a beginner
        or expert, get the right depth of explanation.
      </>
    ),
  },
  {
    title: 'Multi-Language Support',
    icon: '🌍',
    description: (
      <>
        Learn in English or Urdu. High-quality translations help you
        understand complex concepts in your preferred language.
      </>
    ),
  },
];

function Feature({title, icon, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.feature}>
        <div className={styles.featureIcon}>{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}