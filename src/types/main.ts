export type JwtAlgorithm = 'HS256' | 'HS384' | 'HS512' | 'RS256' | 'RS384' | 'RS512'

export interface MercureConfig {
  endpoint: string
  adminToken: string
  jwt: {
    alg: JwtAlgorithm
    secret: string
  }
  http?: {
    timeout?: number
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
