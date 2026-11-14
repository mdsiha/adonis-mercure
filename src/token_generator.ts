import jws from 'jws'
import { MercureError } from './errors/mercure_error.js'
import type { MercureConfig, TokenOptions } from './types/main.js'

export class TokenGenerator {
  #config: MercureConfig

  constructor(config: MercureConfig) {
    this.#config = config
  }

  async generate(payload: Record<string, unknown>, options: TokenOptions = {}): Promise<string> {
    const claims: Record<string, unknown> = { mercure: payload }

    if (options.expiresIn !== undefined) {
      if (!Number.isInteger(options.expiresIn) || options.expiresIn <= 0) {
        throw new MercureError('expiresIn must be a positive integer (seconds)')
      }
      claims.exp = Math.floor(Date.now() / 1000) + options.expiresIn
    }

    return new Promise<string>((resolve, reject) => {
      jws
        .createSign({
          payload: claims,
          secret: this.#config.jwt.secret,
          header: { alg: this.#config.jwt.alg },
        })
        .on('error', reject)
        .on('done', resolve)
    })
  }

  // wildcard topic grants access to all private events, don't pass user input directly
  generateSubscribeToken(topics: string[], options?: TokenOptions): Promise<string> {
    return this.generate({ subscribe: topics }, options)
  }
}
