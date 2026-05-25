import { test } from '@japa/runner'
import { Mercure } from '../src/mercure.js'

const config = {
  endpoint: 'http://localhost:3000/.well-known/mercure',
  adminToken: 'test-admin-token',
  jwt: { alg: 'HS256' as const, secret: 'test-secret-long-enough-for-tests-ok' },
}

test.group('Mercure', (group) => {
  let originalFetch: typeof globalThis.fetch

  group.each.setup(() => {
    originalFetch = globalThis.fetch
  })

  group.each.teardown(() => {
    globalThis.fetch = originalFetch
  })

  test('generate returns a signed JWT string', async ({ assert }) => {
    const mercure = new Mercure(config)
    const token = await mercure.generate({ subscribe: ['/chat/1'] })

    assert.isString(token)
    assert.equal(token.split('.').length, 3)
  })

  test('generateSubscribeToken returns JWT with subscribe claim', async ({ assert }) => {
    const mercure = new Mercure(config)
    const token = await mercure.generateSubscribeToken(['/orders/42'])

    const raw = token.split('.')[1]
    const payload = JSON.parse(Buffer.from(raw, 'base64url').toString())
    assert.deepEqual(payload.mercure.subscribe, ['/orders/42'])
  })

  test('send publishes topic and data to the hub', async ({ assert }) => {
    let capturedBody = ''
    globalThis.fetch = async (_url, init) => {
      capturedBody = (init as RequestInit).body as string
      return new Response('1', { status: 200 })
    }

    await new Mercure(config).send('/topic', { msg: 'hello' })

    const body = new URLSearchParams(capturedBody)
    assert.equal(body.get('topic'), '/topic')
    assert.deepEqual(JSON.parse(body.get('data')!), { msg: 'hello' })
  })

  test('send converts boolean true to private=on', async ({ assert }) => {
    let capturedBody = ''
    globalThis.fetch = async (_url, init) => {
      capturedBody = (init as RequestInit).body as string
      return new Response('1', { status: 200 })
    }

    await new Mercure(config).send('/topic', {}, true)

    const body = new URLSearchParams(capturedBody)
    assert.equal(body.get('private'), 'on')
  })

  test('send accepts a SendOptions object', async ({ assert }) => {
    let capturedBody = ''
    globalThis.fetch = async (_url, init) => {
      capturedBody = (init as RequestInit).body as string
      return new Response('1', { status: 200 })
    }

    await new Mercure(config).send(
      '/topic',
      {},
      { private: true, id: 'evt-1', type: 'order.shipped' }
    )

    const body = new URLSearchParams(capturedBody)
    assert.equal(body.get('private'), 'on')
    assert.equal(body.get('id'), 'evt-1')
    assert.equal(body.get('type'), 'order.shipped')
  })

  test('ping returns true when hub responds', async ({ assert }) => {
    globalThis.fetch = async () => new Response('', { status: 200 })

    assert.isTrue(await new Mercure(config).ping())
  })

  test('ping returns true even on hub 4xx response', async ({ assert }) => {
    globalThis.fetch = async () => new Response('', { status: 401 })

    assert.isTrue(await new Mercure(config).ping())
  })

  test('ping returns false on network error', async ({ assert }) => {
    globalThis.fetch = async () => {
      throw new Error('Network error')
    }

    assert.isFalse(await new Mercure(config).ping())
  })
})
