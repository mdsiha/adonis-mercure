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

export interface TokenOptions {
  /** Token lifetime in seconds. No `exp` claim is set when omitted */
  expiresIn?: number
}

export interface SendOptions {
  private?: boolean
  id?: string
  type?: string
  retry?: number
}

export interface MercureContract {
  generate(payload: Record<string, unknown>, options?: TokenOptions): Promise<string>
  generateSubscribeToken(topics: string[], options?: TokenOptions): Promise<string>
  send(
    topics: string | string[],
    data?: Record<string, unknown>,
    options?: boolean | SendOptions
  ): Promise<Response>
  ping(): Promise<boolean>
}
