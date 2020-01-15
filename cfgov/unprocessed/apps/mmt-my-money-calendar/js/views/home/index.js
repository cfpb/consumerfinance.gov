import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <main className="mmt-view home">
      <h1>Home</h1>
      <Link to="/wizard">Begin Wizard</Link>
    </main>
  );
}
