import jws from 'jws'
import { MercureConfig } from './types/main.js'
import got from 'got'

export class Mercure {
  #config: MercureConfig

  constructor(config: MercureConfig) {
    this.#config = config
  }

  generate(payload: any) {
    return new Promise((resolve, reject) => {
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

  async send(
    topics: string | string[],
    data: Record<string, string> = {},
    isPrivate: boolean = false
  ) {
    topics = Array.isArray(topics) ? topics : [topics]

    const form = new URLSearchParams()

    topics.forEach((topic) => form.append('topic', topic))
    form.append('data', JSON.stringify(data))

    if (isPrivate) {
      form.append('private', 'on')
    }

    try {
      const response = await got.post(this.#config.endpoint, {
        headers: {
          'Authorization': `Bearer ${this.#config.adminToken}`,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: form.toString(),
      })

      return response
    } catch (error) {
      if (error.response) {
        console.error('Error response:', error.response.body)
        console.error('Status code:', error.response.statusCode)
      } else {
        console.error('Error message:', error.message)
      }
    }
  }
}
