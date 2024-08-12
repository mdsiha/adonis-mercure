import type { Algorithm } from 'jws'

export interface MercureConfig {
  endpoint: string
  adminToken: string
  jwt: {
    alg: Algorithm
    secret: string
  }
}
