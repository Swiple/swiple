// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Build Trust in Every Dataset',
  tagline: 'With Swiple, quickly identify and resolve data issues with continuous observability. Avoid the impact of bad data on your business with the only platform that proactively detects issues.',
  url: 'https://swiple.io',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'Swiple', // Usually your GitHub org/user name.
  projectName: 'swiple', // Usually your repo name.
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl: 'https://github.com/Swiple/swiple/blob/main/docs',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            'https://github.com/Swiple/swiple/blob/main/docs',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
        gtag: {
          trackingID: 'G-8PLQFLJQV6',
        }
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Swiple',
        logo: {
          alt: 'Swiple Logo',
          src: 'img/logo.png',
        },
        items: [
          {
            type: 'doc',
            docId: 'introduction',
            position: 'left',
            label: 'Docs',
          },
          // {to: '/blog', label: 'Blog', position: 'left'},
          {
            href: 'https://join.slack.com/t/swiple/shared_invite/zt-1cssnt7k0-51zMQENDhFiDMW2k1jA75g',
            label: 'Slack',
            position: 'right',
          },
          {
            href: 'https://github.com/Swiple/swiple',
            label: 'GitHub',
            position: 'right',
            image: '',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Getting Started',
                to: '/docs/getting-started/quick-start',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/swiple',
              },
              {
                label: 'Slack',
                href: 'https://join.slack.com/t/swiple/shared_invite/zt-1cssnt7k0-51zMQENDhFiDMW2k1jA75g',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/Swiple/swiple.git',
              },
            ],
          },
          {
            title: 'Legal',
            items: [
              {
                label: 'Privacy Policy',
                href: 'https://app.termly.io/document/privacy-policy/ef5398d2-c693-4003-8b58-f04126956851',
              },
              {
                label: 'Terms and Conditions',
                href: 'https://app.termly.io/document/terms-of-use-for-saas/1f642552-e0b1-4a98-9498-1c96daaeb4b1',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Swiple, Ltd. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
