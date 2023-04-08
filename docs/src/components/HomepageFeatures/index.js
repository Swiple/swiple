import React, { useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import { isMobile } from 'react-device-detect';

const FeatureRows = [
  {
    title: 'Automated Data Profiling',
    type: 'video',
    Svg: require('@site/static/img/generate-suggestions.mp4').default,
    subtitle: 'Create tailored checks for each dataset without a data expert',
    description: (
      <>
        Save engineers weeks of time generating data quality checks. Swiple analyzes your dataset and builds data
        quality checks based on what is observed in your data. You just pick the ones you want.
      </>
    ),
  },
  {
    title: 'Data Quality Reporting',
    type: 'video',
    Svg: require('@site/static/img/data-health.mp4').default,
    subtitle: 'Gain a comprehensive view of your data quality health',
    description: (
      <>
        Data teams often encounter unforeseen data quality issues. Understanding past trends empowers them to make
        informed decisions and proactively tackle data challenges.
      </>
    ),
  },
  {
    title: 'Incident Alerting',
    type: 'img',
    Svg: require('@site/static/img/create-action.png').default,
    subtitle: 'Stay ahead of data quality issues',
    description: (
      <>
        Boost your teams efficiency and confidence with Swiple alerting capabilities. Ensure your data teams are the
        first to know about data quality concerns with notifications dispatched to your team as they occur.
      </>
    ),
  },
  {
    title: 'Scheduling',
    type: 'video',
    Svg: require('@site/static/img/create-schedule.mp4').default,
    subtitle: 'Effortless scheduling for seamless data validations',
    description: (
      <>
        Built in scheduling enables autonomous data validations at any recurrence interval, allowing for easy
        integration into your data pipeline.
      </>
    ),
  },
];

function Text({ title, subtitle, description, idx }) {
  const color = idx % 2 === 0 ? '#1990FF' : '#1FD1A9';
  return (
    <div className={clsx('col col--6', styles.text, styles.textCenter)}>
      <div className="d-flex flex-column justify-content-center h-100">
        <div className="padding-horiz--md">
          <h3 style={{ color: color }}>{title}</h3>
          <h1>{subtitle}</h1>
          <p style={{ fontSize: 18, lineHeight: '1.5em', color: '#343741' }}>{description}</p>
        </div>
      </div>
    </div>
  )
}

function Image({ Svg, type }) {
  const videoRef = useRef(null);

  useEffect(() => {
    if (type !== 'video') return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            videoRef.current.play();
          } else {
            videoRef.current.pause();
          }
        });
      },
      { threshold: 0.5 }
    );

    observer.observe(videoRef.current);

    return () => {
      observer.disconnect();
    };
  }, [type]);

  return (
    <div className={clsx('col col--6')}>
      <div>
        {type === 'img' ? (
          <img src={Svg} role="img" />
        ) : (
          <video
            ref={videoRef}
            src={Svg}
            playsInline
            muted={true}
            autoPlay={false}
            controls={false}
            loop={true}
            className={clsx(styles.video, styles.dropShadow)}
          />
        )}
      </div>
    </div>
  );
}

const isSmallScreen = () => {
  return isMobile || window.innerWidth <= 996;
};


function Feature({ Svg, title, type, subtitle, description, idx }) {
  const text = <Text title={title} subtitle={subtitle} description={description} idx={idx} />;
  const image = <Image Svg={Svg} type={type} />;

  const renderForSmallScreen = isSmallScreen()
  const LeftSide = idx % 2 === 0 || renderForSmallScreen ? text : image;
  const RightSide = idx % 2 === 0 || renderForSmallScreen ? image : text;

  return (
    <>
      <div className={clsx('row feature-container', styles.feature)}>
        {LeftSide}
        {RightSide}
      </div>
      <div className={clsx('row')} style={{ height: 160 }} />
    </>
  );
}



export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className={clsx('row')} style={{ height: 60 }} />
        <div className="row">
          <div className="col col--8 col--offset-2 text--center">
            <h1>
              Zero-infrastructure. Zero-code setup.
            </h1>
            <p style={{ fontSize: 18, lineHeight: '1.5em', color: '#343741' }}>
              Experience hassle-free integration with Swiple's zero-infrastructure and
              zero-code setup. Seamlessly incorporate data quality checks into your existing
              workflows without any coding or infrastructure changes, allowing you to focus
              on what matters most - your data.
            </p>
          </div>
        </div>
        <div className={clsx('row')} style={{ height: 120 }} />
        {FeatureRows.map((props, idx) => (
          <Feature key={`feature-${idx}`} {...props} idx={idx} />
        ))}
      </div>
    </section>
  );
}
