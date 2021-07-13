export interface WaterTankPayload {
  readonly type: 'water_tank';
}

export interface LightPayload {
  readonly type: 'light';
  readonly power: boolean;
}

export interface UnknownPayload {
  readonly type: string;
  readonly [k: string]: any;
}

export type Payload = LightPayload | WaterTankPayload | UnknownPayload;

export interface Message {
  readonly id: string;
  readonly registered: string;
  readonly last_updated: string;
  readonly last_payload: Payload;
}
