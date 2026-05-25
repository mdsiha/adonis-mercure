import jws from 'jws'
import type { MercureConfig } from './types/main.js'

export class TokenGenerator {
  #config: MercureConfig

  constructor(config: MercureConfig) {
    this.#config = config
  }

  generate(payload: Record<string, unknown>): Promise<string> {
    return new Promise<string>((resolve, reject) => {
      jws
        .createSign({
          payload: { mercure: payload },
          secret: this.#config.jwt.secret,
          header: { alg: this.#config.jwt.alg },
        })
        .on('error', reject)
        .on('done', resolve)
    })
  }

  generateSubscribeToken(topics: string[]): Promise<string> {
    return this.generate({ subscribe: topics })
  }
}
