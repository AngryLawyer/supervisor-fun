import React from 'react';
import { useListPoll } from './hooks/useListPoll';
import { useSendMessage } from './hooks/useSendMessage';
import Device from './devices/Device';
import { DateTime } from 'luxon';

function App() {
  const items = useListPoll();
  const sendMessage = useSendMessage();
  const currentDateTime = DateTime.utc();
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
            {items.map(item => <Device key={item.id} message={item} currentDateTime={currentDateTime} sendMessage={sendMessage}/>)}
          </div>
        </div>
      </div>
    </main>
    </>
  );
}

export default App;
