export type Payload = {};

export interface Message {
  readonly id: string;
  readonly registered: string;
  readonly last_updated: string;
  readonly last_payload: Payload;
}
