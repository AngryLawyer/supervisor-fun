import React from 'react';
import { Duration } from 'luxon';
import { Message, LightPayload } from '../types';
import BaseDevice from './BaseDevice';
import { ReactComponent as Lamp } from './lamp.svg';
import './lamp.scss';

interface Props {
  payload: LightPayload;
  message: Message;
  timeSinceLastUpdate: Duration
}

export default ({ payload, message, timeSinceLastUpdate}: Props) => {
  const lightState = `Light is ${payload.power ? 'On' : 'Off'}`;
  return (
    <BaseDevice
      header={<Lamp width={320} height={320} className={`bd-placeholder-img card-img-top lamp ${payload.power ? 'on' : 'off'}`}/>}
      title={message.id}
      text={lightState}
      timeSinceLastUpdate={timeSinceLastUpdate}
    />
  );
}
