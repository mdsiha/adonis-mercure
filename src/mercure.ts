import { TokenGenerator } from './token_generator.js'
import { Publisher } from './publisher.js'
import type { MercureConfig, MercureContract, SendOptions } from './types/main.js'

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

  generate(payload: Record<string, unknown>): Promise<string> {
    return this.#tokenGenerator.generate(payload)
  }

  generateSubscribeToken(topics: string[]): Promise<string> {
    return this.#tokenGenerator.generateSubscribeToken(topics)
  }

  send(
    topics: string | string[],
    data: Record<string, unknown> = {},
    isPrivateOrOptions: boolean | SendOptions = false
  ): Promise<Response> {
    const options: SendOptions =
      typeof isPrivateOrOptions === 'boolean' ? { private: isPrivateOrOptions } : isPrivateOrOptions

    return this.#publisher.publish(topics, data, options)
  }

  async ping(): Promise<boolean> {
    const timeout = this.#config.http?.timeout ?? DEFAULT_TIMEOUT
    const controller = timeout > 0 ? new AbortController() : null
    const timer = controller ? setTimeout(() => controller.abort(), timeout) : null

    try {
      await fetch(this.#config.endpoint, {
        method: 'HEAD',
        signal: controller?.signal,
      })
      return true
    } catch {
      return false
    } finally {
      if (timer) clearTimeout(timer)
    }
  }
}
