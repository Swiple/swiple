import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import SupportedDatabases from '@site/src/components/SupportedDatabases';
import ExpectationsList from '../components/Expectations';


function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div>
          <Link
            className="button button--secondary button--lg margin-right--md"
            to="/docs/installation/quick-start">
            Get Started in 4 Commands 🚀
          </Link>
          <Link
            className={clsx("button button--secondary button--lg", styles.buttonStar)}
            to="/docs/installation/quick-start">
            Give Swiple a Star ⭐️
          </Link>
        </div>
        <div className={clsx("margin-bottom--xl")} />
        <video
            poster={require('@site/static/img/swiple-demo-video-poster.png').default}
            src="https://swiple.io/video/swiple-demo-video.mp4"
            playsInline
            muted={false}
            autoPlay={false}
            controls
            className={clsx(styles.demoVideo)}
        />
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Description will go into a meta tag in <head />"
    >
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <ExpectationsList />
        <SupportedDatabases />
      </main>
    </Layout>
  );
}
