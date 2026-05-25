export class MercureError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'MercureError'
  }
}
