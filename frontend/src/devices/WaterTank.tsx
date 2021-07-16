import React from 'react';
import { Duration } from 'luxon';
import { Message, WaterTankPayload } from '../types';
import BaseDevice from './BaseDevice';
import WaterTankSVG from './graphics/WaterTank';

interface Props {
  payload: WaterTankPayload;
  message: Message;
  timeSinceLastUpdate: Duration
}

export default ({ payload, message, timeSinceLastUpdate}: Props) => {
  return (
    <BaseDevice
      header={<WaterTankSVG width={320} height={320} className="bd-placeholder-img card-img-top" waterLevel={payload.water_level}/>}
      title={message.id}
      timeSinceLastUpdate={timeSinceLastUpdate}
      actions={payload.actions}
    />
  );
}

