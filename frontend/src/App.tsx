import React from 'react';
import { useListPoll } from './hooks/useListPoll';
import Default from './devices/Default';

function App() {
  const items = useListPoll();
  return (
    <>
      <header>
        <div className="navbar navbar-dark bg-dark shadow-sm">
          <div className="container">
            <strong className="navbar-brand">Dashboard</strong>
          </div>
        </div>
      </header>
      <main>
      <div className="py-5 bg-light">
        <div className="container">
          <div className="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
            {items.map(item => <Default key={item.id}/>)}
          </div>
        </div>
      </div>
    </main>
    </>
  );
}

export default App;
