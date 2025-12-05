import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <h1 className={styles.heroTitle}>
              🤖 Physical AI Textbook
            </h1>
            <p className={styles.heroSubtitle}>
              Master the complete stack of autonomous robotics: from real-time control with ROS 2 to intelligent perception with NVIDIA Isaac, and natural language understanding with Vision-Language-Action systems.
            </p>
            <div className={styles.heroButtons}>
              <Link
                className={clsx('button button--lg', styles.buttonPrimary)}
                to="/docs/intro">
                Start Learning →
              </Link>
              <Link
                className={clsx('button button--lg', styles.buttonSecondary)}
                to="/docs/module-1-ros2">
                Explore Modules
              </Link>
            </div>
          </div>
          <div className={styles.heroImage}>
            <div className={styles.robotAnimation}>
              <svg viewBox="0 0 200 200" className={styles.robot}>
                {/* Robot Head */}
                <circle cx="100" cy="50" r="20" fill="#00d4ff" opacity="0.8"/>
                {/* Eyes */}
                <circle cx="92" cy="45" r="3" fill="#fff"/>
                <circle cx="108" cy="45" r="3" fill="#fff"/>
                {/* Torso */}
                <rect x="85" y="75" width="30" height="40" rx="5" fill="#0066cc" opacity="0.8"/>
                {/* Left Arm */}
                <rect x="60" y="80" width="25" height="10" rx="5" fill="#00d4ff" opacity="0.8"/>
                {/* Right Arm */}
                <rect x="115" y="80" width="25" height="10" rx="5" fill="#00d4ff" opacity="0.8"/>
                {/* Left Leg */}
                <rect x="80" y="120" width="8" height="50" rx="4" fill="#0066cc" opacity="0.8"/>
                {/* Right Leg */}
                <rect x="112" y="120" width="8" height="50" rx="4" fill="#0066cc" opacity="0.8"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

const ModuleCard = ({title, icon, description, link, color}) => (
  <Link to={link} className={styles.moduleLink}>
    <div className={clsx(styles.moduleCard, styles[`module_${color}`])}>
      <div className={styles.moduleIcon}>{icon}</div>
      <h3 className={styles.moduleTitle}>{title}</h3>
      <p className={styles.moduleDescription}>{description}</p>
      <div className={styles.moduleArrow}>→</div>
    </div>
  </Link>
);

function ModulesSection() {
  const modules = [
    {
      title: 'Module 1: ROS 2',
      icon: '🔌',
      description: 'The Robotic Nervous System - Learn nodes, topics, services, and URDF.',
      link: '/docs/module-1-ros2',
      color: 'blue'
    },
    {
      title: 'Module 2: Digital Twin',
      icon: '🌐',
      description: 'Gazebo & Unity - Physics simulation and high-fidelity rendering.',
      link: '/docs/module-2-digital-twin',
      color: 'purple'
    },
    {
      title: 'Module 3: Isaac AI',
      icon: '🧠',
      description: 'The AI-Robot Brain - VSLAM, path planning, and perception.',
      link: '/docs/module-3-isaac',
      color: 'green'
    },
    {
      title: 'Module 4: VLA',
      icon: '🗣️',
      description: 'Vision-Language-Action - Voice commands and autonomous tasks.',
      link: '/docs/module-4-vla',
      color: 'orange'
    },
  ];

  return (
    <section className={styles.modulesSection}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2>📚 Learning Modules</h2>
          <p>Complete the journey from robotics basics to autonomous humanoids</p>
        </div>
        <div className={styles.modulesGrid}>
          {modules.map((module, idx) => (
            <ModuleCard key={idx} {...module} />
          ))}
        </div>
      </div>
    </section>
  );
}

const FeatureCard = ({icon, title, description}) => (
  <div className={styles.featureCard}>
    <div className={styles.featureIcon}>{icon}</div>
    <h3>{title}</h3>
    <p>{description}</p>
  </div>
);

function FeaturesSection() {
  return (
    <section className={styles.featuresSection}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2>✨ Why Physical AI?</h2>
          <p>Everything you need for autonomous robotics</p>
        </div>
        <div className={styles.featuresGrid}>
          <FeatureCard
            icon="💻"
            title="Practical Code"
            description="Copy-paste ready Python examples for every concept"
          />
          <FeatureCard
            icon="🚀"
            title="Industry Standard"
            description="Learn tools used by Tesla, Boston Dynamics, and OpenAI"
          />
          <FeatureCard
            icon="🔗"
            title="Integrated Stack"
            description="ROS 2 → Gazebo → Isaac Sim → LLMs in one textbook"
          />
          <FeatureCard
            icon="🎓"
            title="Capstone Project"
            description="Build a fully autonomous humanoid robot"
          />
          <FeatureCard
            icon="🤝"
            title="Open Source"
            description="CC-BY-4.0 licensed. Contribute and remix freely"
          />
          <FeatureCard
            icon="🌍"
            title="Community"
            description="Learn from roboticists building the future"
          />
        </div>
      </div>
    </section>
  );
}

function CurriculumSection() {
  return (
    <section className={styles.curriculumSection}>
      <div className="container">
        <h2>🎯 Your Learning Path</h2>
        <div className={styles.curriculumTimeline}>
          <div className={styles.timelineItem}>
            <div className={styles.timelineDot}/>
            <div className={styles.timelineContent}>
              <h4>Weeks 1-2: ROS 2 Fundamentals</h4>
              <p>Master robot middleware, pub/sub patterns, and URDF</p>
            </div>
          </div>
          <div className={styles.timelineItem}>
            <div className={styles.timelineDot}/>
            <div className={styles.timelineContent}>
              <h4>Weeks 3-4: Digital Twins</h4>
              <p>Simulate robots in Gazebo with realistic sensors</p>
            </div>
          </div>
          <div className={styles.timelineItem}>
            <div className={styles.timelineDot}/>
            <div className={styles.timelineContent}>
              <h4>Weeks 5-6: AI Perception</h4>
              <p>VSLAM, path planning, and autonomous navigation</p>
            </div>
          </div>
          <div className={styles.timelineItem}>
            <div className={styles.timelineDot}/>
            <div className={styles.timelineContent}>
              <h4>Weeks 7-8: Capstone</h4>
              <p>Build your autonomous humanoid with voice control</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function StatsSection() {
  return (
    <section className={styles.statsSection}>
      <div className="container">
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <div className={styles.statNumber}>2000+</div>
            <div className={styles.statLabel}>Lines of Code</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statNumber}>50+</div>
            <div className={styles.statLabel}>Practical Examples</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statNumber}>4</div>
            <div className={styles.statLabel}>Complete Modules</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statNumber}>1</div>
            <div className={styles.statLabel}>Capstone Project</div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className={styles.ctaSection}>
      <div className="container">
        <div className={styles.ctaContent}>
          <h2>Ready to Build Your First Autonomous Robot?</h2>
          <p>Join thousands of roboticists learning the complete Physical AI stack</p>
          <Link
            className={clsx('button button--lg', styles.ctaButton)}
            to="/docs/intro">
            Start the Textbook Now →
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title} - Learn Autonomous Robotics`}
      description="Complete textbook for Physical AI and autonomous robotics. Master ROS 2, digital twins, perception, and language-guided robot control.">
      <HomepageHeader />
      <main>
        <ModulesSection />
        <StatsSection />
        <FeaturesSection />
        <CurriculumSection />
        <CTASection />
      </main>
    </Layout>
  );
}
