const Hero = ({ title, subtitle, image, alt = '' }) => {
  const imageTag = (typeof image === 'string') ? <img src={image} alt={alt} className="u-hide-on-print" /> : image;

  return (
    <section className="m-hero">
      <div className="m-hero_wrapper wrapper">
        <div className="m-hero_text">
          <h1 className="m-hero_heading">{title}</h1>
          <div className="m-hero_subhead">
            {subtitle}
          </div>
        </div>
        <div className="m-hero_image-wrapper">
          <div className="m-hero_image">
            {imageTag}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
