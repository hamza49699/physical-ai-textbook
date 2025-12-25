import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/physical-ai-textbook/__docusaurus/debug',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug', '1b0'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/config',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/config', '4ef'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/content',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/content', '02c'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/globalData',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/globalData', '58f'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/metadata',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/metadata', '647'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/registry',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/registry', '125'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/routes',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/routes', 'aa1'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/markdown-page',
    component: ComponentCreator('/physical-ai-textbook/markdown-page', '0c3'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/docs',
    component: ComponentCreator('/physical-ai-textbook/docs', '682'),
    routes: [
      {
        path: '/physical-ai-textbook/docs',
        component: ComponentCreator('/physical-ai-textbook/docs', 'e72'),
        routes: [
          {
            path: '/physical-ai-textbook/docs',
            component: ComponentCreator('/physical-ai-textbook/docs', '06b'),
            routes: [
              {
                path: '/physical-ai-textbook/docs/intro',
                component: ComponentCreator('/physical-ai-textbook/docs/intro', '14c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-1-intro',
                component: ComponentCreator('/physical-ai-textbook/docs/module-1-intro', '222'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-1-ros2',
                component: ComponentCreator('/physical-ai-textbook/docs/module-1-ros2', '867'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-2-digital-twin',
                component: ComponentCreator('/physical-ai-textbook/docs/module-2-digital-twin', '275'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-2-intro',
                component: ComponentCreator('/physical-ai-textbook/docs/module-2-intro', '55b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-3-intro',
                component: ComponentCreator('/physical-ai-textbook/docs/module-3-intro', '405'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-3-isaac',
                component: ComponentCreator('/physical-ai-textbook/docs/module-3-isaac', '6c0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-4-intro',
                component: ComponentCreator('/physical-ai-textbook/docs/module-4-intro', 'cd6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-4-vla',
                component: ComponentCreator('/physical-ai-textbook/docs/module-4-vla', '1ad'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-5-intro',
                component: ComponentCreator('/physical-ai-textbook/docs/module-5-intro', '87f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-6-intro',
                component: ComponentCreator('/physical-ai-textbook/docs/module-6-intro', '0f1'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/physical-ai-textbook/',
    component: ComponentCreator('/physical-ai-textbook/', '94f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
