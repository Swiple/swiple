import React, { useEffect } from 'react';
import { loadStripeScript } from './loadStripeScript';

const StripePricingTable = () => {
  useEffect(() => {
    const loadScript = async () => {
      try {
        await loadStripeScript();
      } catch (error) {
        console.error('Error loading Stripe script:', error);
      }
    };

    loadScript();
  }, []);

  return (
    <stripe-pricing-table
      pricing-table-id="prctbl_1MqzvqEegVmkNFJd0nLeEgXQ"
      publishable-key="pk_live_51MqyxhEegVmkNFJdYb7jUYboM5cEMifhFoMpZ7Wo9g5KAUeiV9M4UJ0Q8I72CJf9Vk8VazALHGmyFMVOCIxrlOwt00xXJanhG8"
    ></stripe-pricing-table>
  );
};

export default StripePricingTable;
