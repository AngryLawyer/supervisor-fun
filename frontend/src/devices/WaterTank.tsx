import React from "react";
import { Duration } from "luxon";
import { Message, WaterTankPayload, Action } from "../types";
import BaseDevice from "./BaseDevice";
import WaterTankSVG from "./graphics/WaterTank";

interface Props {
  payload: WaterTankPayload;
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
  return (
    <BaseDevice
      header={
        <WaterTankSVG
          width={320}
          height={320}
          className="bd-placeholder-img card-img-top"
          waterLevel={payload.water_level}
        />
      }
      title={message.id}
      timeSinceLastUpdate={timeSinceLastUpdate}
      actions={payload.actions}
      sendMessage={sendMessage}
      id={message.id}
    />
  );
};
