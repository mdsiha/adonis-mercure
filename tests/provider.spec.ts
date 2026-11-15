import { test } from '@japa/runner'
import { Container } from '@adonisjs/core/container'
import { Mercure } from '../src/mercure.js'
import { MercureConfigError } from '../src/errors/config_error.js'
import MercureProvider from '../providers/mercure_provider.js'

const config = {
  endpoint: 'http://localhost:3000/.well-known/mercure',
  adminToken: 'test-admin-token',
  jwt: { alg: 'HS256' as const, secret: 'test-secret-long-enough-for-tests-ok' },
}

function makeProvider(mercureConfig: unknown) {
  const container = new Container<any>()
  const app = { container, config: { get: () => mercureConfig } }
  return { container, provider: new MercureProvider(app as any) }
}

test.group('MercureProvider', () => {
  test('binds a Mercure instance in the container', async ({ assert }) => {
    const { container, provider } = makeProvider(config)
    await provider.boot()

    assert.instanceOf(await container.make('mercure'), Mercure)
  })

  test('returns the same instance on every resolve', async ({ assert }) => {
    const { container, provider } = makeProvider(config)
    await provider.boot()

    assert.strictEqual(await container.make('mercure'), await container.make('mercure'))
  })

  test('throws MercureConfigError when the config is missing', async ({ assert }) => {
    const { container, provider } = makeProvider(undefined)
    await provider.boot()

    const error = await container.make('mercure').catch((e: unknown) => e)

    assert.instanceOf(error, MercureConfigError)
    assert.match((error as Error).message, /Missing or incomplete Mercure config/)
  })

  test('throws when the config is incomplete', async ({ assert }) => {
    const { container, provider } = makeProvider({ ...config, adminToken: '' })
    await provider.boot()

    const error = await container.make('mercure').catch((e: unknown) => e)

    assert.instanceOf(error, MercureConfigError)
  })
})
