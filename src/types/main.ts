import type { Algorithm } from 'jws'

export interface MercureConfig {
  endpoint: string
  adminToken: string
  jwt: {
    alg: Algorithm
    secret: string
  }
}

export interface SendOptions {
  private?: boolean
  id?: string
  type?: string
  retry?: number
}

export interface MercureContract {
  generate(payload: Record<string, unknown>): Promise<string>
  generateSubscribeToken(topics: string[]): Promise<string>
  send(
    topics: string | string[],
    data?: Record<string, unknown>,
    options?: boolean | SendOptions
  ): Promise<Response>
  ping(): Promise<boolean>
}
