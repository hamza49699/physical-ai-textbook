import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Essential Guide to Physical AI and Humanoid Robotics',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://hamza49699.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/physical-ai-textbook/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'hamza49699', // Usually your GitHub org/user name.
  projectName: 'physical-ai-textbook', // Usually your repo name.
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',

  // Custom environment variables for client-side access
  customFields: {
    backendUrl: process.env.REACT_APP_BACKEND_URL || 'https://hamzakhan123-physical-ai-textbook.hf.space',
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/hamza49699/physical-ai-textbook/tree/main',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl:
            'https://github.com/hamza49699/physical-ai-textbook/tree/main',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: '🤖 Physical AI',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Learn',
        },
        {
          label: 'Modules',
          position: 'left',
          items: [
            {
              label: 'Module 1: ROS 2',
              to: '/docs/module-1-ros2',
            },
            {
              label: 'Module 2: Digital Twin',
              to: '/docs/module-2-digital-twin',
            },
            {
              label: 'Module 3: Isaac AI',
              to: '/docs/module-3-isaac',
            },
            {
              label: 'Module 4: VLA',
              to: '/docs/module-4-vla',
            },
          ],
        },
        {to: '/blog', label: 'Resources', position: 'left'},
        {
          href: 'https://github.com/hamza49699/physical-ai-textbook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Curriculum',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Module 1: ROS 2',
              to: '/docs/module-1-ros2',
            },
            {
              label: 'Module 2: Digital Twin',
              to: '/docs/module-2-digital-twin',
            },
            {
              label: 'Module 3: Isaac AI',
              to: '/docs/module-3-isaac',
            },
            {
              label: 'Module 4: VLA',
              to: '/docs/module-4-vla',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub Discussions',
              href: 'https://github.com/hamza49699/physical-ai-textbook/discussions',
            },
            {
              label: 'Report Issues',
              href: 'https://github.com/hamza49699/physical-ai-textbook/issues',
            },
            {
              label: 'Contribute',
              href: 'https://github.com/hamza49699/physical-ai-textbook/pulls',
            },
            {
              label: 'Discord',
              href: 'https://discord.gg/robotics',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'ROS 2 Documentation',
              href: 'https://docs.ros.org/en/humble/',
            },
            {
              label: 'NVIDIA Isaac',
              href: 'https://docs.nvidia.com/isaac/',
            },
            {
              label: 'Gazebo Sim',
              href: 'http://gazebosim.org/',
            },
            {
              label: 'OpenAI API',
              href: 'https://platform.openai.com/docs/',
            },
          ],
        },
        {
          title: 'Legal',
          items: [
            {
              label: 'CC-BY-4.0 License',
              href: 'https://creativecommons.org/licenses/by/4.0/',
            },
            {
              label: 'Source Code',
              href: 'https://github.com/hamza49699/physical-ai-textbook',
            },
          ],
        },
      ],
      copyright: `© ${new Date().getFullYear()} Physical AI Textbook. Made with ❤️ for roboticists. Licensed under CC-BY-4.0.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
