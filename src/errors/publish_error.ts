import { MercureError } from './mercure_error.js'

export class MercurePublishError extends MercureError {
  constructor(
    readonly statusCode: number,
    readonly responseBody: string
  ) {
    super(`Mercure hub returned ${statusCode}: ${responseBody}`)
    this.name = 'MercurePublishError'
  }
}
