import { MercureError } from './mercure_error.js'

export class MercurePublishError extends MercureError {
  readonly responseBody: string

  constructor(
    readonly statusCode: number,
    responseBody: string
  ) {
    super(`Mercure hub returned ${statusCode}`)
    this.name = 'MercurePublishError'
    this.responseBody = responseBody.slice(0, 200)
  }
}
