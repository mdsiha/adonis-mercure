import { MercureConfigError } from './errors/config_error.js'
import type { JwtAlgorithm, JwtConfig, MercureConfig } from './types/main.js'

const ALLOWED_PROTOCOLS: readonly string[] = ['0.x', '1.x']

const ALLOWED_ALGORITHMS: readonly JwtAlgorithm[] = [
  'HS256',
  'HS384',
  'HS512',
  'RS256',
  'RS384',
  'RS512',
]

function isHttpUrl(value: string): boolean {
  try {
    const { protocol } = new URL(value)
    return protocol === 'http:' || protocol === 'https:'
  } catch {
    return false
  }
}

function validateJwt(jwt: JwtConfig, name: string): void {
  if (!ALLOWED_ALGORITHMS.includes(jwt.alg)) {
    throw new MercureConfigError(
      `Algorithm "${jwt.alg}" is not allowed. Use one of: ${ALLOWED_ALGORITHMS.join(', ')}`
    )
  }

  if (jwt.secret.length < 32) {
    throw new MercureConfigError(`${name}.secret must be at least 32 characters long`)
  }
}

function validate(config: MercureConfig): void {
  if (config.protocol !== undefined && !ALLOWED_PROTOCOLS.includes(config.protocol)) {
    throw new MercureConfigError(`protocol must be one of: ${ALLOWED_PROTOCOLS.join(', ')}`)
  }

  if (!isHttpUrl(config.endpoint)) {
    throw new MercureConfigError('endpoint must be a valid http(s) URL')
  }

  validateJwt(config.jwt, 'jwt')

  if (config.protocol !== '1.x') {
    if (!config.adminToken) {
      throw new MercureConfigError(`adminToken must not be empty`)
    }
    return
  }

  if (!config.issuer) {
    throw new MercureConfigError(`issuer must not be empty`)
  }

  // optional in 1.x, but an empty value is a mistake
  if (config.adminToken === '') {
    throw new MercureConfigError(`adminToken must not be empty`)
  }

  if (config.publisherJwt) {
    validateJwt(config.publisherJwt, 'publisherJwt')
  }

  if (config.audience !== undefined) {
    const audiences = [config.audience].flat()

    if (audiences.length === 0 || audiences.some((audience) => !audience)) {
      throw new MercureConfigError(`audience must not be empty`)
    }
  }
}

export function defineConfig<T extends MercureConfig>(config: T): T {
  validate(config)

  return config
}
