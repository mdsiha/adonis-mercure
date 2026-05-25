import { MercureError } from './mercure_error.js'

export class MercureConfigError extends MercureError {
  constructor(message: string) {
    super(message)
    this.name = 'MercureConfigError'
  }
}
