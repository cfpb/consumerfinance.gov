import { Link, useRouteMatch } from "react-router-dom";

export default function Hero() {
  // Interval will be either month or week

  return (
    <section class="m-hero">
      <div class="m-hero_wrapper wrapper">
        <div class="m-hero_text">
          <h1 class="m-hero_heading">My Money Calendar</h1>
          <div class="m-hero_subhead">
            Visualize your spending and learn strategies to manage your weekly
            and monthly budget{" "}
          </div>
        </div>
        <div class="m-hero_image-wrapper">
          <div class="m-hero_image">
            <img
              src="/static/apps/mmt-my-money-calendar/img/Hero_2.png"
              alt=""
              class="u-hide-on-print"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
