import { test } from '@japa/runner'
import { TokenGenerator } from '../src/token_generator.js'

const config = {
  endpoint: 'http://localhost:3000/.well-known/mercure',
  adminToken: 'test-token',
  jwt: { alg: 'HS256' as const, secret: 'test-secret' },
}

test.group('TokenGenerator', () => {
  test('generate returns a JWT string', async ({ assert }) => {
    const generator = new TokenGenerator(config)
    const token = await generator.generate({ subscribe: ['*'] })

    assert.isString(token)
    assert.equal(token.split('.').length, 3)
  })

  test('generated token contains the mercure claim', async ({ assert }) => {
    const generator = new TokenGenerator(config)
    const token = await generator.generate({ subscribe: ['/chat/1'] })

    const raw = token.split('.')[1]
    const payload = JSON.parse(Buffer.from(raw, 'base64url').toString())

    assert.deepEqual(payload.mercure.subscribe, ['/chat/1'])
  })

  test('generateSubscribeToken wraps topics in subscribe field', async ({ assert }) => {
    const generator = new TokenGenerator(config)
    const token = await generator.generateSubscribeToken(['/orders/42'])

    const raw = token.split('.')[1]
    const payload = JSON.parse(Buffer.from(raw, 'base64url').toString())

    assert.deepEqual(payload.mercure.subscribe, ['/orders/42'])
  })
})
