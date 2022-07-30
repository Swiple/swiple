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
        {/*<h1 className="hero__title">{siteConfig.title}</h1>*/}
        {/*<p className="hero__subtitle">{siteConfig.tagline}</p>*/}
        {/*<div className={styles.buttons}>*/}
        {/*  <Link*/}
        {/*    className="button button--secondary button--lg"*/}
        {/*    to="/docs/installation/quick-start.md">*/}
        {/*    Get Started*/}
        {/*  </Link>*/}
        {/*</div>*/}
        <div className="row">
          <div className="col col--6" style={{position: "relative", marginBottom: 50}}>
            <h1 className="hero__title">{siteConfig.title}</h1>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
            <div className={styles.buttons}>
              <Link
                className="button button--secondary button--lg"
                to="/docs/installation/quick-start">
                Get Started
              </Link>
            </div>
          </div>
          <div className="col col--6" style={{float: "left", position: "relative"}}>
            <video playsInline muted autoPlay loop="true">
              <source src={require('@site/static/videos/video-home-observability.mp4').default} type="video/mp4"/>
            </video>
            {/*<img*/}
            {/*  src={require('@site/static/img/dashboard.png').default}*/}
            {/*  role="img"*/}
            {/*/>*/}
          </div>
        </div>
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
