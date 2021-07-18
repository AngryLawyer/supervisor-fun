export interface Action {
  readonly id: string;
  readonly label: string;
}

export interface WaterTankPayload {
  readonly template: "water_tank";
  readonly water_level: number;
  readonly actions: readonly Action[];
}

export interface LightPayload {
  readonly template: "light";
  readonly power: boolean;
  readonly actions: readonly Action[];
}

export interface UnknownPayload {
  readonly template: string;
  readonly actions: readonly Action[];
  readonly [k: string]: any;
}

export type Payload = LightPayload | WaterTankPayload | UnknownPayload;

export interface Message {
  readonly id: string;
  readonly registered: string;
  readonly last_updated: string;
  readonly last_payload: Payload;
}
