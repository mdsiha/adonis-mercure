import { test } from '@japa/runner'
import { defineConfig } from '../src/define_config.js'
import { MercureConfigError } from '../src/errors/config_error.js'

const validConfig = {
  endpoint: 'http://localhost:3000/.well-known/mercure',
  adminToken: 'test-admin-token',
  jwt: { alg: 'HS256' as const, secret: 'test-secret-long-enough-for-tests-ok' },
}

test.group('defineConfig', () => {
  test('returns the config untouched when valid', ({ assert }) => {
    assert.strictEqual(defineConfig(validConfig), validConfig)
  })

  test('throws a MercureConfigError', ({ assert }) => {
    try {
      defineConfig({ ...validConfig, adminToken: '' })
      assert.fail('expected defineConfig to throw')
    } catch (error) {
      assert.instanceOf(error, MercureConfigError)
    }
  })

  test('rejects an unsupported algorithm', ({ assert }) => {
    const config = { ...validConfig, jwt: { ...validConfig.jwt, alg: 'none' as any } }

    assert.throws(() => defineConfig(config), /is not allowed/)
  })

  test('rejects a secret shorter than 32 characters', ({ assert }) => {
    const config = { ...validConfig, jwt: { ...validConfig.jwt, secret: 'too-short' } }

    assert.throws(() => defineConfig(config), /at least 32 characters/)
  })

  test('rejects an endpoint that is not a URL', ({ assert }) => {
    const config = { ...validConfig, endpoint: 'not a url' }

    assert.throws(() => defineConfig(config), /valid http\(s\) URL/)
  })

  test('rejects an endpoint with another protocol', ({ assert }) => {
    const config = { ...validConfig, endpoint: 'ftp://localhost/.well-known/mercure' }

    assert.throws(() => defineConfig(config), /valid http\(s\) URL/)
  })

  test('rejects an empty adminToken', ({ assert }) => {
    const config = { ...validConfig, adminToken: '' }

    assert.throws(() => defineConfig(config), /adminToken must not be empty/)
  })
})
