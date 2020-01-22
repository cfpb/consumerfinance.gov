import heroImg from 'img/Hero_2.png';

export default function Hero() {
  // Interval will be either month or week

  return (
    <section className="m-hero">
      <div className="m-hero_wrapper wrapper">
        <div className="m-hero_text">
          <h1 className="m-hero_heading">My Money Calendar</h1>
          <div className="m-hero_subhead">
            Visualize your spending and learn strategies to manage your weekly and monthly budget{' '}
          </div>
        </div>
        <div className="m-hero_image-wrapper">
          <div className="m-hero_image">
            <img src={heroImg} alt="" className="u-hide-on-print" />
          </div>
        </div>
      </div>
    </section>
  );
}

export default Hero;
