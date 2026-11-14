import { test } from '@japa/runner'
import { TokenGenerator } from '../src/token_generator.js'

const config = {
  endpoint: 'http://localhost:3000/.well-known/mercure',
  adminToken: 'test-token',
  jwt: { alg: 'HS256' as const, secret: 'test-secret' },
}

function decode(token: string) {
  return JSON.parse(Buffer.from(token.split('.')[1], 'base64url').toString())
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

  test('token has no exp claim by default', async ({ assert }) => {
    const token = await new TokenGenerator(config).generateSubscribeToken(['/orders/42'])

    assert.isUndefined(decode(token).exp)
  })

  test('expiresIn sets the exp claim in seconds from now', async ({ assert }) => {
    const before = Math.floor(Date.now() / 1000)
    const token = await new TokenGenerator(config).generateSubscribeToken(['/orders/42'], {
      expiresIn: 3600,
    })
    const after = Math.floor(Date.now() / 1000)

    const { exp } = decode(token)
    assert.isAtLeast(exp, before + 3600)
    assert.isAtMost(exp, after + 3600)
  })

  test('generate accepts expiresIn too', async ({ assert }) => {
    const token = await new TokenGenerator(config).generate({ subscribe: ['*'] }, { expiresIn: 60 })

    assert.isNumber(decode(token).exp)
  })

  test('expiresIn rejects zero, negative and non-integer values', async ({ assert }) => {
    const generator = new TokenGenerator(config)

    for (const expiresIn of [0, -5, 1.5, Number.NaN]) {
      await assert.rejects(
        () => generator.generate({ subscribe: ['*'] }, { expiresIn }),
        'expiresIn must be a positive integer (seconds)'
      )
    }
  })
})
