import { useState, useCallback } from 'react';

function Counter({ initial = 0 }) {
  const [count, setCount] = useState(initial);

  const increment = useCallback((evt) => {
    evt.preventDefault();
    setCount(count + 1);
  }, []);
  const decrement = useCallback((evt) => {
    evt.preventDefault();
    setCount(count - 1);
  }, []);

  return (
    <div className="counter">
      <h2>Counter</h2>
      <button onClick={decrement}>--</button>
      <strong>{count}</strong>
      <button onClick={increment}>++</button>
    </div>
  );
}

export default Counter;
