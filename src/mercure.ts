import { TokenGenerator } from './token_generator.js'
import { Publisher } from './publisher.js'
import type { MercureConfig, MercureContract, SendOptions, TokenOptions } from './types/main.js'

const DEFAULT_TIMEOUT = 5000

export class Mercure implements MercureContract {
  #config: MercureConfig
  #tokenGenerator: TokenGenerator
  #publisher: Publisher

  constructor(config: MercureConfig) {
    this.#config = config
    this.#tokenGenerator = new TokenGenerator(config)
    this.#publisher = new Publisher(config)
  }

  generate(payload: Record<string, unknown>, options?: TokenOptions): Promise<string> {
    return this.#tokenGenerator.generate(payload, options)
  }

  generateSubscribeToken(topics: string[], options?: TokenOptions): Promise<string> {
    return this.#tokenGenerator.generateSubscribeToken(topics, options)
  }

  send(
    topics: string | string[],
    data: Record<string, unknown> = {},
    isPrivateOrOptions: boolean | SendOptions = false
  ): Promise<string> {
    const options: SendOptions =
      typeof isPrivateOrOptions === 'boolean' ? { private: isPrivateOrOptions } : isPrivateOrOptions

    return this.#publisher.publish(topics, data, options)
  }

  async ping(): Promise<boolean> {
    const timeout = this.#config.http?.timeout ?? DEFAULT_TIMEOUT
    const controller = timeout > 0 ? new AbortController() : null
    const timer = controller ? setTimeout(() => controller.abort(), timeout) : null

    try {
      const response = await fetch(this.#config.endpoint, {
        method: 'HEAD',
        signal: controller?.signal,
      })

      // 4xx still means the hub answered
      return response.status < 500
    } catch {
      return false
    } finally {
      if (timer) clearTimeout(timer)
    }
  }
}
