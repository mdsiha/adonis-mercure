import type { MercureContract, SendOptions } from './types/main.js'

export interface SentMessage {
  topics: string[]
  data: Record<string, unknown>
  options: SendOptions
}

export class FakeMercure implements MercureContract {
  #sent: SentMessage[] = []
  #tokens: Array<Record<string, unknown>> = []

  async generate(payload: Record<string, unknown>): Promise<string> {
    this.#tokens.push(payload)
    return 'fake-token'
  }

  async generateSubscribeToken(topics: string[]): Promise<string> {
    return this.generate({ subscribe: topics })
  }

  async send(
    topics: string | string[],
    data: Record<string, unknown> = {},
    isPrivateOrOptions: boolean | SendOptions = false
  ): Promise<Response> {
    const topicList = Array.isArray(topics) ? topics : [topics]
    const options: SendOptions =
      typeof isPrivateOrOptions === 'boolean' ? { private: isPrivateOrOptions } : isPrivateOrOptions

    this.#sent.push({ topics: topicList, data, options })
    return new Response('1', { status: 200 })
  }

  async ping(): Promise<boolean> {
    return true
  }

  assertSent(topic: string, data?: Record<string, unknown>): void {
    const match = this.#sent.find((msg) => {
      if (!msg.topics.includes(topic)) return false
      if (!data) return true
      return JSON.stringify(msg.data) === JSON.stringify(data)
    })

    if (!match) {
      const found = this.#sent.map((m) => m.topics.join(', ')).join('; ') || 'nothing'
      throw new Error(`Expected a message on topic "${topic}" but found: [${found}]`)
    }
  }

  assertNotSent(topic: string): void {
    const match = this.#sent.find((msg) => msg.topics.includes(topic))
    if (match) {
      throw new Error(`Expected no message on topic "${topic}" but one was found`)
    }
  }

  assertNothingSent(): void {
    if (this.#sent.length > 0) {
      const topics = this.#sent.map((m) => m.topics.join(', ')).join('; ')
      throw new Error(`Expected nothing to be sent but found messages on: [${topics}]`)
    }
  }

  getSent(): SentMessage[] {
    return [...this.#sent]
  }

  clear(): void {
    this.#sent = []
    this.#tokens = []
  }
}
