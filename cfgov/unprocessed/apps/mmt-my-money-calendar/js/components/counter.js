import { useState, useCallback } from 'react';

function Counter({ initial = 0 }) {
  const [count, setCount] = useState(initial);

  const increment = useCallback((evt) => {
    evt.preventDefault();
    setCount(count + 1);
  }, [count]);
  const decrement = useCallback((evt) => {
    evt.preventDefault();
    setCount(count - 1);
  }, [count]);

  return (
    <div className="counter">
      <h2>Counter</h2>
      <button onClick={decrement}>--</button>
      <br />
      <strong>{count}</strong>
      <br />
      <button onClick={increment}>++</button>
    </div>
  );
}

export default Counter;
