import { MercureError } from './mercure_error.js'

export class MercureConnectionError extends MercureError {
  constructor(cause: unknown) {
    super(`Could not reach the Mercure hub: ${describe(cause)}`, { cause })
    this.name = 'MercureConnectionError'
  }
}

// fetch() throws a generic "fetch failed" and hides the real reason in `cause.code`
function describe(error: unknown): string {
  const code = (error as { cause?: { code?: string } })?.cause?.code
  if (code) return code
  return error instanceof Error ? error.message : String(error)
}
