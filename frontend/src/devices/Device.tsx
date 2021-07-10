import React from 'react';
import { Message } from '../types';
import Default from './Default';

interface Props {
  message: Message;
}

export default ({ message }: Props) => {
  return (
    <Default payload={message.last_payload}/>
  );
}

