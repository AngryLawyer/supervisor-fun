import React from 'react';
import { Duration } from 'luxon';
import humanizeDuration from 'humanize-duration';
import { Action } from '../types';
import './baseDevice.scss';

const EXPIRE_TIME = 10;

interface Props {
  title: string;
  text?: string;
  body?: React.ReactNode;
  header?: React.ReactNode;
  timeSinceLastUpdate: Duration;
  actions: readonly Action[];
}

export default ({text, body, header, timeSinceLastUpdate, title, actions}: Props) => {
  const hasExpired = timeSinceLastUpdate.shiftTo('seconds').get('seconds') > EXPIRE_TIME;
  
  return (
    <div className={`col base-device ${hasExpired ? 'disconnected' : ''}`}>
      <div className="card shadow-sm">
        {header}
        <div className="card-body">
          <h5>{title}</h5>
          { text && <p className="card-text">{text}</p> }
          { body }
          <div className="d-flex justify-content-between align-items-center">
            <div className="btn-group">
              {actions.map(a => (
                <button type="button" className="btn btn-sm btn-outline-secondary">{a.label}</button>
              ))}
            </div>
            <small className="text-muted">Last updated { humanizeDuration(timeSinceLastUpdate.valueOf(), { round: true }) } ago</small>
          </div>
        </div>
      </div>
    </div>
  );
}

