import { Link } from "react-router-dom";

export default function Home() {
  // This is the Home Page of the app
  return (
    <main className="mmt-view home">
      <h1>Home</h1>
      <Link to="/wizard/steps/starting-balance">Begin Wizard</Link>
    </main>
  );
}
