import { MercureConfig } from './types/main.js'

export function defineConfig<T extends MercureConfig>(config: T): T {
  return config
}
