import React from "react";
import { Duration } from "luxon";
import { Message, LightPayload, Action } from "../types";
import BaseDevice from "./BaseDevice";
import Lamp from "./graphics/Lamp";

interface Props {
  payload: LightPayload;
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
  const lightState = `Light is ${payload.power ? "On" : "Off"}`;
  return (
    <BaseDevice
      header={
        <Lamp
          width={320}
          height={320}
          className="bd-placeholder-img card-img-top lamp"
          fill={payload.power ? "red" : "black"}
        />
      }
      title={message.id}
      text={lightState}
      timeSinceLastUpdate={timeSinceLastUpdate}
      actions={payload.actions}
      sendMessage={sendMessage}
      id={message.id}
    />
  );
};
