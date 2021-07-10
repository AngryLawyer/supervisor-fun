import React from 'react';
import { DateTime } from 'luxon';
import { UnknownPayload } from '../types';
import BaseDevice from './BaseDevice';

interface Props {
  payload: UnknownPayload;

}

export default ({ payload }: Props) => {
  const body = (
    <ul>
      {Object.entries(payload).map(([k, v]) => (
        <li key={k}>{k}: {v}</li>
      ))}
    </ul>
  );
  return (
    <BaseDevice
      body={body}
    />
  );
}
