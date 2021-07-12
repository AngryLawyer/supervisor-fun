import React from 'react';
import { DateTime, Interval } from 'luxon';
import { LightPayload, Message } from '../types';
import Default from './Default';
import Light from './Light';

interface Props {
  message: Message;
  currentDateTime: DateTime
}

export default ({ message, currentDateTime }: Props) => {
  const timeSinceLastUpdate = Interval.fromDateTimes(DateTime.fromISO(message.last_updated), currentDateTime).toDuration();
  switch (message.last_payload.type) {
    case 'light':
      return (
        <Light payload={message.last_payload as LightPayload} message={message} timeSinceLastUpdate={timeSinceLastUpdate} />
      );
    default:
      return (
        <Default payload={message.last_payload} message={message} timeSinceLastUpdate={timeSinceLastUpdate} />
      );
  }
}

