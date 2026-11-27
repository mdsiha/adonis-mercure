import { MercureConnectionError } from './errors/connection_error.js'
import { MercureError } from './errors/mercure_error.js'
import { MercurePublishError } from './errors/publish_error.js'
import { MercureTimeoutError } from './errors/timeout_error.js'
import { TokenGenerator } from './token_generator.js'
import type { MercureConfig, SendOptions } from './types/main.js'

const DEFAULT_TIMEOUT = 5000
const PUBLISHER_TOKEN_LIFETIME = 300
// renew before the hub can see an expired token
const PUBLISHER_TOKEN_MARGIN = 60

export class Publisher {
  #config: MercureConfig
  #cachedToken?: { value: string; renewAt: number }

  constructor(config: MercureConfig) {
    this.#config = config
  }

  async publish(
    topics: string | string[],
    data: Record<string, unknown> = {},
    options: SendOptions = {}
  ): Promise<string> {
    const topicList = Array.isArray(topics) ? topics : [topics]
    const form = new URLSearchParams()

    for (const topic of topicList) {
      form.append('topic', topic)
    }
    form.append('data', JSON.stringify(data))

    if (options.private) form.append('private', 'on')
    if (options.id) form.append('id', options.id)
    if (options.type) form.append('type', options.type)
    if (options.retry !== undefined) form.append('retry', String(options.retry))

    const token = await this.#publisherToken()
    const timeout = this.#config.http?.timeout ?? DEFAULT_TIMEOUT
    const controller = timeout > 0 ? new AbortController() : null
    const timer = controller ? setTimeout(() => controller.abort(), timeout) : null

    try {
      const response = await fetch(this.#config.endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: form.toString(),
        signal: controller?.signal,
      })

      if (!response.ok) {
        const body = await response.text()
        throw new MercurePublishError(response.status, body)
      }

      const id = await response.text()
      return id.trim()
    } catch (err) {
      if (err instanceof MercureError) throw err
      if ((err as Error)?.name === 'AbortError') {
        throw new MercureTimeoutError(timeout)
      }
      throw new MercureConnectionError(err)
    } finally {
      if (timer) clearTimeout(timer)
    }
  }

  // the configured adminToken, or in 1.x a short-lived token signed by the package
  async #publisherToken(): Promise<string> {
    const config = this.#config

    if (config.protocol !== '1.x') return config.adminToken
    if (config.adminToken) return config.adminToken

    if (this.#cachedToken && Date.now() < this.#cachedToken.renewAt) {
      return this.#cachedToken.value
    }

    const renewAt = Date.now() + (PUBLISHER_TOKEN_LIFETIME - PUBLISHER_TOKEN_MARGIN) * 1000
    const generator = new TokenGenerator({ ...config, jwt: config.publisherJwt ?? config.jwt })
    const value = await generator.generate(
      { publish: ['*'] },
      { expiresIn: PUBLISHER_TOKEN_LIFETIME, subject: config.issuer }
    )
    this.#cachedToken = { value, renewAt }

    return value
  }
}
