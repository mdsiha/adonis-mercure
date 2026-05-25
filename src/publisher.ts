import { MercurePublishError } from './errors/publish_error.js'
import type { MercureConfig, SendOptions } from './types/main.js'

export class Publisher {
  #config: MercureConfig

  constructor(config: MercureConfig) {
    this.#config = config
  }

  async publish(
    topics: string | string[],
    data: Record<string, unknown> = {},
    options: SendOptions = {}
  ): Promise<Response> {
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

    const response = await fetch(this.#config.endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.#config.adminToken}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: form.toString(),
    })

    if (!response.ok) {
      const body = await response.text()
      throw new MercurePublishError(response.status, body)
    }

    return response
  }
}
