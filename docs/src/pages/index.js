import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import ExpectationsList from '../components/Expectations';
import Carousel from '../components/Carousel';
import Pricing from '../components/Pricing';
import HeroGradient from '../components/HeroGradient';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx(styles.heroBanner)}>
      <HeroGradient />
      <div className="container">
        <h1 className="hero__title" style={{ color: '#fff' }}>
          Data Quality in Hours<br />Not Months
        </h1>

        <p className="hero__subtitle" style={{color: '#fff'}}>
          {siteConfig.tagline}
        </p>
        <div>
          <Link
            className="button button--secondary button--lg margin-right--md"
            to="https://calendly.com/swiple/swiple-cloud-demo"
          >
            <div style={{display: "flex"}}>
              Book a demo 🚀
            </div>
          </Link>
          <Link
            className={clsx("button button--secondary button--lg margin-right--md", styles.buttonStar)}
            to="/docs/getting-started/quick-start">
            Run locally in 4 steps 💻
          </Link>
          {/*<Link*/}
          {/*  className={clsx("button button--secondary button--lg", styles.buttonStar)}*/}
          {/*  href="https://github.com/Swiple/swiple">*/}
          {/*  Give Swiple a Star ⭐️*/}
          {/*</Link>*/}
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
      description="Swiple is an automated data monitoring platform that helps analytics and data engineering teams seamlessly monitor the quality of their data.
With automated data analysis and profiling, scheduling and alerting, teams can resolve data quality issues before they impact mission critical resources."
    >
      <HomepageHeader />
      <main>
        <Carousel />
        <HomepageFeatures />
        <ExpectationsList />
        <Pricing />
      </main>
    </Layout>
  );
}
