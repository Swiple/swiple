import React from 'react';
import StripePricingTable from '../StripePricingTable';
import clsx from 'clsx';

const Pricing = () => {
  return (
    <section style={{ paddingTop: '4rem', paddingBottom: '4rem'}}>
      <div className="container">
        <div className="row">
          <div className="col col--8 col--offset-2 text--center">
            <h1>
              Choose the perfect plan for your data team
            </h1>
            <p style={{ fontSize: 18, lineHeight: '1.5em', color: '#343741' }}>
              Discover the benefits of Swiple with our flexible and cost-effective pricing plans,
              designed to suit data teams of all sizes and requirements.
            </p>
          </div>
        </div>
        <div className={clsx('row')} style={{ height: 60 }} />
        <StripePricingTable />
      </div>
    </section>
  );
};

export default Pricing;
