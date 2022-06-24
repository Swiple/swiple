import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureRow1 = [
  {
    title: 'Automated Data Profiling',
    Svg: require('@site/static/img/automated-profiling.svg').default,
    description: (
      <>
        Swiple profiles your data and automatically generates a suite of expectations based on what is observed in your data.
      </>
    ),
  },
  {
    title: 'Data Validation',
    Svg: require('@site/static/img/data-processing.svg').default,
    description: (
      <>
        Validate your suite of expectations and see which ones passed or failed.
      </>
    ),
  },
  {
    title: 'Data Docs',
    Svg: require('@site/static/img/documentation.svg').default,
    description: (
      <>
        Swiple renders your expectations to clean, readable documentation so you can determine what matters at a glance.
      </>
    ),
  },
];

const FeatureRow2 = [
  {
    title: 'Scheduling',
    Svg: require('@site/static/img/scheduling.svg').default,
    description: (
      <>
        Built-in scheduling functionality allows for automatic data validations on any recurrence interval.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureRow1.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
        <div className="margin-bottom--lg" />
        <div className="row" style={{ justifyContent: "center" }}>
          {FeatureRow2.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
