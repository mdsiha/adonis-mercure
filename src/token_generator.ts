import { randomUUID } from 'node:crypto'
import jws from 'jws'
import { MercureError } from './errors/mercure_error.js'
import type {
  MercureConfig,
  ModernMercureConfig,
  TokenOptions,
  TopicMatcher,
} from './types/main.js'

const AUTHORIZATION_DETAIL_TYPE = 'https://mercure.rocks/authorization-detail'
const DEFAULT_EXPIRES_IN = 3600
const ACTIONS = ['publish', 'subscribe'] as const
const ALLOWED_KEYS: readonly string[] = [...ACTIONS, 'payload']

function expirationFrom(now: number, expiresIn: number): number {
  if (!Number.isInteger(expiresIn) || expiresIn <= 0) {
    throw new MercureError('expiresIn must be a positive integer (seconds)')
  }

  return now + expiresIn
}

// turns one topic into the matcher object expected by a 1.x hub
function toMatcher(topic: unknown) {
  if (typeof topic === 'string') {
    if (/\{[^}]*\}/.test(topic)) {
      throw new MercureError(
        `URI templates are not supported by Mercure 1.x: "${topic}". Use { match: '/orders/:id', matchType: 'urlpattern' }`
      )
    }

    return { match: topic }
  }

  const { match, matchType } = (topic ?? {}) as { match?: unknown; matchType?: unknown }

  if (typeof match !== 'string' || (matchType !== 'exact' && matchType !== 'urlpattern')) {
    throw new MercureError(
      'A topic must be a string or { match, matchType: "exact" | "urlpattern" }'
    )
  }

  return matchType === 'urlpattern' ? { match, match_type: matchType } : { match }
}

function toAuthorizationDetails(payload: Record<string, unknown>) {
  const unknownKey = Object.keys(payload).find((key) => !ALLOWED_KEYS.includes(key))

  if (unknownKey) {
    throw new MercureError(`Unknown key "${unknownKey}". Use one of: ${ALLOWED_KEYS.join(', ')}`)
  }

  const details: Array<Record<string, unknown>> = []

  for (const action of ACTIONS) {
    const topics = payload[action]

    if (topics === undefined) continue

    if (!Array.isArray(topics)) {
      throw new MercureError(`${action} must be an array of topics`)
    }

    if (topics.length === 0) continue

    const detail: Record<string, unknown> = {
      type: AUTHORIZATION_DETAIL_TYPE,
      actions: [action],
      topics: topics.map(toMatcher),
    }

    if (action === 'subscribe' && payload.payload !== undefined) {
      detail.payload = payload.payload
    }

    details.push(detail)
  }

  if (payload.payload !== undefined && !details.some((detail) => 'payload' in detail)) {
    throw new MercureError('payload requires at least one subscribe topic')
  }

  return details
}

function assertStringTopics(payload: Record<string, unknown>): void {
  for (const action of ACTIONS) {
    const topics = payload[action]

    if (Array.isArray(topics) && topics.some((topic) => typeof topic !== 'string')) {
      throw new MercureError("Topic matcher objects require protocol '1.x'")
    }
  }
}

export class TokenGenerator {
  #config: MercureConfig

  constructor(config: MercureConfig) {
    this.#config = config
  }

  async generate(payload: Record<string, unknown>, options: TokenOptions = {}): Promise<string> {
    const config = this.#config

    if (config.protocol === '1.x') {
      return this.#sign(this.#accessTokenClaims(config, payload, options), 'at+jwt')
    }

    assertStringTopics(payload)

    const claims: Record<string, unknown> = { mercure: payload }

    if (options.expiresIn !== undefined) {
      claims.exp = expirationFrom(Math.floor(Date.now() / 1000), options.expiresIn)
    }

    return this.#sign(claims)
  }

  generateSubscribeToken(
    topics: Array<string | TopicMatcher>,
    options?: TokenOptions
  ): Promise<string> {
    return this.generate({ subscribe: topics }, options)
  }

  // claims of an RFC 9068 access token
  #accessTokenClaims(
    config: ModernMercureConfig,
    payload: Record<string, unknown>,
    options: TokenOptions
  ): Record<string, unknown> {
    const now = Math.floor(Date.now() / 1000)

    return {
      iss: config.issuer,
      aud: config.audience ?? config.endpoint,
      sub: options.subject ?? `urn:uuid:${randomUUID()}`,
      client_id: config.issuer,
      iat: now,
      exp: expirationFrom(now, options.expiresIn ?? DEFAULT_EXPIRES_IN),
      jti: `urn:uuid:${randomUUID()}`,
      authorization_details: toAuthorizationDetails(payload),
    }
  }

  #sign(claims: Record<string, unknown>, typ?: string): Promise<string> {
    return new Promise<string>((resolve, reject) => {
      jws
        .createSign({
          payload: claims,
          secret: this.#config.jwt.secret,
          header: { alg: this.#config.jwt.alg, ...(typ && { typ }) },
        })
        .on('error', reject)
        .on('done', resolve)
    })
  }
}
