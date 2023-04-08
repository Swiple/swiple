import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';


const SupportedDatabases = [
  {
    title: 'Snowflake',
    Svg: require('@site/static/img/databases/snowflake-icon.png').default,
    height: 60,
    width: 60,
  },
  {
    title: 'BigQuery',
    Svg: require('@site/static/img/databases/bigquery-icon.png').default,
    height: 60,
    width: 60,
  },
  {
    title: 'Redshift',
    Svg: require('@site/static/img/databases/redshift.png').default,
    height: 60,
    width: 60,
  },
  {
    title: 'PostgreSQL',
    Svg: require('@site/static/img/databases/postgresql.png').default,
    height: 60,
    width: 60,
  },
  {
    title: 'Trino',
    Svg: require('@site/static/img/databases/trino.png').default,
    height: 60,
    width: 60,
  },
  {
    title: 'Athena',
    Svg: require('@site/static/img/databases/athena.png').default,
    height: 60,
    width: 60,
  },
  {
    title: 'MySQL',
    Svg: require('@site/static/img/databases/mysql.png').default,
    height: 90,
    width: 90,
  },
];

function Database({ Svg, width, height }) {
  return (
    <img
      src={Svg}
      style={{height, width}}
      role="img"
    />
  );
}

export default function Carousel() {
  const settings = {
    slidesToShow: 5,
    autoplay: true,
    autoplaySpeed: 0,
    speed: 5000,
    cssEase:'linear',
    infinite: true,
    focusOnSelect: false,
    useTransform: false,
    arrows: false,
    responsive: [{
        breakpoint: 996,
        settings: {
          arrows: false,
          slidesToShow: 3,
          speed: 2000,
        }
    }, {
        breakpoint: 480,
        settings: {
          arrows: false,
          slidesToShow: 3,
          speed: 2000,
        }
    }]
  };

  const tripledSupportedDatabases = [...SupportedDatabases, ...SupportedDatabases, ...SupportedDatabases];

  return (
    <div style={{ backgroundColor: '#F5F7FA', textAlign: 'center', paddingTop: 80, paddingBottom: 80 }}>
      <h1 style={{ textAlign: 'center', marginBottom: 50 }}>Platforms we support</h1>
      <Slider {...settings}>
        {tripledSupportedDatabases.map((props, index) => (
          <div key={`carousel-${index}`}>
            <Database {...props} />
          </div>
        ))}
      </Slider>
    </div>
  );
}
