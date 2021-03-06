import React from "react";
import { Duration } from "luxon";
import { Message, UnknownPayload, Action } from "../types";
import BaseDevice from "./BaseDevice";

interface Props {
  payload: UnknownPayload;
  message: Message;
  timeSinceLastUpdate: Duration;
  sendMessage: (id: string, action: Action) => void;
}

export default ({
  payload,
  message,
  timeSinceLastUpdate,
  sendMessage,
}: Props) => {
  const body = (
    <ul>
      {Object.entries(payload).map(([k, v]) => (
        <li key={k}>
          {k}: {v}
        </li>
      ))}
    </ul>
  );
  return (
    <BaseDevice
      title={message.id}
      body={body}
      timeSinceLastUpdate={timeSinceLastUpdate}
      actions={payload.actions}
      sendMessage={sendMessage}
      id={message.id}
    />
  );
};
