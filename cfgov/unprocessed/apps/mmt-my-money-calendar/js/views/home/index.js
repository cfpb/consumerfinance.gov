import { Link } from "react-router-dom";
import Hero from "./hero";

export default function Home() {
  // This is the Home Page of the app
  return (
    <main className="mmt-view home">
      <Hero />
      <br />
      <div class="m-hero_subhead">
        Input your income, expenses, and cash-on-hand to build your calendar,
        Estimates are acceptable.
      </div>
      <br />
      <Link to="/wizard/steps/starting-balance">
        Get started with your calendar
      </Link>
      <br />
      <br />
    </main>
  );
}
