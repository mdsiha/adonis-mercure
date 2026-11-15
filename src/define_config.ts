import { MercureConfigError } from './errors/config_error.js'
import type { JwtAlgorithm, MercureConfig } from './types/main.js'

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

export function defineConfig<T extends MercureConfig>(config: T): T {
  if (!ALLOWED_ALGORITHMS.includes(config.jwt.alg)) {
    throw new MercureConfigError(
      `Algorithm "${config.jwt.alg}" is not allowed. Use one of: ${ALLOWED_ALGORITHMS.join(', ')}`
    )
  }

  if (!isHttpUrl(config.endpoint)) {
    throw new MercureConfigError('endpoint must be a valid http(s) URL')
  }

  if (!config.adminToken) {
    throw new MercureConfigError('adminToken must not be empty')
  }

  if (config.jwt.secret.length < 32) {
    throw new MercureConfigError('jwt.secret must be at least 32 characters long')
  }

  return config
}
