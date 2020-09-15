import { useState, useMemo } from 'react';

const Hero = ({ title, subtitle, isSVG = false, image, alt = '' }) => {
  let imageTag;

  if (isSVG && typeof image === 'string') {
    imageTag = <img src={`data:image/svg+xml;base64,${btoa(image)}`} className='u-hide-on-print hero-image' />;
  } else if (typeof image === 'string') {
    imageTag = <img src={image} alt={alt} className='u-hide-on-print hero-image' />;
  } else {
    imageTag = image;
  }

  return (
    <section className='m-hero'>
      <div className='m-hero_wrapper wrapper'>
        <div className='m-hero_text'>
          <h1 className='m-hero_heading'>{title}</h1>
          <div className='m-hero_subhead'>{subtitle}</div>
        </div>
        <div className='m-hero_image-wrapper'>
          <div className='m-hero_image' style={{ textAlign: 'center' }}>
            {imageTag}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
