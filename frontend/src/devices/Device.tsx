import React from "react";
import { DateTime, Interval } from "luxon";
import { LightPayload, WaterTankPayload, Message, Action } from "../types";
import Default from "./Default";
import Light from "./Light";
import WaterTank from "./WaterTank";

interface Props {
  message: Message;
  currentDateTime: DateTime;
  sendMessage: (id: string, action: Action) => void;
}

export default ({ message, currentDateTime, sendMessage }: Props) => {
  const timeSinceLastUpdate = Interval.fromDateTimes(
    DateTime.fromISO(message.last_updated),
    currentDateTime
  ).toDuration();
  switch (message.last_payload.template) {
    case "light":
      return (
        <Light
          payload={message.last_payload as LightPayload}
          message={message}
          timeSinceLastUpdate={timeSinceLastUpdate}
          sendMessage={sendMessage}
        />
      );
    case "water_tank":
      return (
        <WaterTank
          payload={message.last_payload as WaterTankPayload}
          message={message}
          timeSinceLastUpdate={timeSinceLastUpdate}
          sendMessage={sendMessage}
        />
      );
    default:
      return (
        <Default
          payload={message.last_payload}
          message={message}
          timeSinceLastUpdate={timeSinceLastUpdate}
          sendMessage={sendMessage}
        />
      );
  }
};
