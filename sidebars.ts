import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-intro',
        'module-1-ros2',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-intro',
        'module-2-digital-twin',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module-3-intro',
        'module-3-isaac',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4-intro',
        'module-4-vla',
      ],
    },
    {
      type: 'category',
      label: 'Module 5: Advanced Humanoid Control',
      items: [
        'module-5-intro',
      ],
    },
    {
      type: 'category',
      label: 'Module 6: Autonomous Systems & Deployment',
      items: [
        'module-6-intro',
      ],
    },
  ],
};

export default sidebars;
