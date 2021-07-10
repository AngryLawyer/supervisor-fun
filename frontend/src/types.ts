export interface UnknownPayload {
  readonly type: string;
  readonly [k: string]: any;
}

export type Payload = UnknownPayload;

export interface Message {
  readonly id: string;
  readonly registered: string;
  readonly last_updated: string;
  readonly last_payload: Payload;
}
