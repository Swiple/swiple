import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
      title: 'PostgreSQL',
        Svg: require('@site/static/img/databases/postgresql.png').default,
      //   height: 200,
      // width: 200,
      height: 100,
        width: 100,
    },
    {
        title: 'Snowflake',
        Svg: require('@site/static/img/databases/snowflake-icon.png').default,
        // height: 200,
        // width: 200,
        height: 100,
        width: 100,
    },
    {
        title: 'Redshift',
        Svg: require('@site/static/img/databases/redshift.png').default,
        height: 100,
        width: 100,
    },
    {
        title: 'Athena',
        Svg: require('@site/static/img/databases/athena.png').default,
        height: 100,
        width: 100,
    },
    {
        title: 'MySQL',
        Svg: require('@site/static/img/databases/mysql.png').default,
        height: 180,
        width: 180,
    },
];

function Feature({Svg, title, height, width}) {
  return (
    <div className={clsx('col col--4 margin-bottom--lg')}>
      <div className={`text--center ${styles.centeredImg}`}>
        <img
            src={Svg}
            style={{ height, width }}
            className={styles.featureSvg}
            role="img"
        />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        {/*<p>{description}</p>*/}
      </div>
    </div>
  );
}

export default function SupportedDatabases() {
  return (
    <section className={styles.features}>
      <div className="container">
          <h1>Supported Databases</h1>
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
