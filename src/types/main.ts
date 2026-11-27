export type JwtAlgorithm = 'HS256' | 'HS384' | 'HS512' | 'RS256' | 'RS384' | 'RS512'

export interface JwtConfig {
  alg: JwtAlgorithm
  secret: string
}

interface BaseMercureConfig {
  endpoint: string
  jwt: JwtConfig
  http?: {
    timeout?: number
  }
}

export interface LegacyMercureConfig extends BaseMercureConfig {
  protocol?: '0.x'
  adminToken: string
}

export interface ModernMercureConfig extends BaseMercureConfig {
  protocol: '1.x'
  issuer: string
  audience?: string | string[]
  publisherJwt?: JwtConfig
  adminToken?: string
}

export type MercureConfig = LegacyMercureConfig | ModernMercureConfig

export interface TopicMatcher {
  match: string
  matchType: 'exact' | 'urlpattern'
}

export interface TokenOptions {
  /** Token lifetime in seconds. No `exp` claim is set when omitted */
  expiresIn?: number
  /** `sub` claim, 1.x only. A random `urn:uuid:` is used when omitted */
  subject?: string
}

export interface SendOptions {
  private?: boolean
  id?: string
  type?: string
  retry?: number
}

export interface MercureContract {
  generate(payload: Record<string, unknown>, options?: TokenOptions): Promise<string>
  generateSubscribeToken(
    topics: Array<string | TopicMatcher>,
    options?: TokenOptions
  ): Promise<string>
  send(
    topics: string | string[],
    data?: Record<string, unknown>,
    options?: boolean | SendOptions
  ): Promise<string>
  ping(): Promise<boolean>
}
