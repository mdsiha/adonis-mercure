/*
|--------------------------------------------------------------------------
| Package entrypoint
|--------------------------------------------------------------------------
*/
export { configure } from './configure.js'
export { Mercure } from './src/mercure.js'
export { FakeMercure } from './src/fake_mercure.js'
export { defineConfig } from './src/define_config.js'
export { stubsRoot } from './stubs/main.js'
export { MercureError } from './src/errors/mercure_error.js'
export { MercurePublishError } from './src/errors/publish_error.js'
export { MercureConfigError } from './src/errors/config_error.js'
export { MercureTimeoutError } from './src/errors/timeout_error.js'
export { MercureConnectionError } from './src/errors/connection_error.js'
export type {
  JwtAlgorithm,
  MercureConfig,
  MercureContract,
  SendOptions,
  TokenOptions,
} from './src/types/main.js'
export type { SentMessage } from './src/fake_mercure.js'
