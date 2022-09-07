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
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/installation/quick-start">
            Get Started in 4 Commands
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
