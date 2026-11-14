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

export function defineConfig<T extends MercureConfig>(config: T): T {
  if (!ALLOWED_ALGORITHMS.includes(config.jwt.alg)) {
    throw new MercureConfigError(
      `Algorithm "${config.jwt.alg}" is not allowed. Use one of: ${ALLOWED_ALGORITHMS.join(', ')}`
    )
  }

  if (config.jwt.secret.length < 32) {
    throw new MercureConfigError('jwt.secret must be at least 32 characters long')
  }

  return config
}
