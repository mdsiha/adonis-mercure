import { MercureError } from './mercure_error.js'

export class MercureTimeoutError extends MercureError {
  constructor(readonly timeoutMs: number) {
    super(`Request to Mercure hub timed out after ${timeoutMs}ms`)
    this.name = 'MercureTimeoutError'
  }
}
