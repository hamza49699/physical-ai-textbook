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
      label: 'Chapter 1: Introduction to Physical AI',
      items: [
        'tutorial-basics/create-a-document',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: Humanoid Robotics Basics',
      items: [
        'tutorial-basics/create-a-page',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 3: ROS 2 Fundamentals',
      items: [
        'tutorial-basics/markdown-features',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 4: Digital Twin Simulation',
      items: [
        'tutorial-extras/manage-docs-versions',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 5: Vision-Language-Action Systems',
      items: [
        'tutorial-extras/translate-your-site',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 6: Capstone Project',
      items: [
        'tutorial-basics/deploy-your-site',
      ],
    },
  ],
};

export default sidebars;
