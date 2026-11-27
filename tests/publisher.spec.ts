import jws from 'jws'
import { test } from '@japa/runner'
import { Publisher } from '../src/publisher.js'
import { MercurePublishError } from '../src/errors/publish_error.js'
import { MercureTimeoutError } from '../src/errors/timeout_error.js'
import { MercureError } from '../src/errors/mercure_error.js'
import { MercureConnectionError } from '../src/errors/connection_error.js'

const config = {
  endpoint: 'http://localhost:3000/.well-known/mercure',
  adminToken: 'test-token',
  jwt: { alg: 'HS256' as const, secret: 'test-secret' },
}

test.group('Publisher', (group) => {
  let originalFetch: typeof globalThis.fetch

  group.each.setup(() => {
    originalFetch = globalThis.fetch
  })

  group.each.teardown(() => {
    globalThis.fetch = originalFetch
  })

  test('posts to the configured endpoint', async ({ assert }) => {
    let capturedUrl: string | URL | Request = ''

    globalThis.fetch = async (url, _init) => {
      capturedUrl = url
      return new Response('1', { status: 200 })
    }

    const publisher = new Publisher(config)
    await publisher.publish('test-topic', { hello: 'world' })

    assert.equal(capturedUrl, config.endpoint)
  })

  test('returns the id sent back by the hub', async ({ assert }) => {
    globalThis.fetch = async () => new Response('urn:uuid:1234\n', { status: 200 })

    const id = await new Publisher(config).publish('test-topic', {})

    assert.equal(id, 'urn:uuid:1234')
  })

  test('sends topic and data in the body', async ({ assert }) => {
    let capturedBody = ''

    globalThis.fetch = async (_url, init) => {
      capturedBody = (init as RequestInit).body as string
      return new Response('1', { status: 200 })
    }

    const publisher = new Publisher(config)
    await publisher.publish('my-topic', { msg: 'hello' })

    const body = new URLSearchParams(capturedBody)
    assert.equal(body.get('topic'), 'my-topic')
    assert.deepEqual(JSON.parse(body.get('data')!), { msg: 'hello' })
  })

  test('appends private=on when option is set', async ({ assert }) => {
    let capturedBody = ''

    globalThis.fetch = async (_url, init) => {
      capturedBody = (init as RequestInit).body as string
      return new Response('1', { status: 200 })
    }

    await new Publisher(config).publish('topic', {}, { private: true })

    const body = new URLSearchParams(capturedBody)
    assert.equal(body.get('private'), 'on')
  })

  test('appends id, type, retry when provided', async ({ assert }) => {
    let capturedBody = ''

    globalThis.fetch = async (_url, init) => {
      capturedBody = (init as RequestInit).body as string
      return new Response('1', { status: 200 })
    }

    await new Publisher(config).publish(
      'topic',
      {},
      { id: 'msg-1', type: 'order.created', retry: 5000 }
    )

    const body = new URLSearchParams(capturedBody)
    assert.equal(body.get('id'), 'msg-1')
    assert.equal(body.get('type'), 'order.created')
    assert.equal(body.get('retry'), '5000')
  })

  test('throws MercurePublishError on non-2xx response', async ({ assert }) => {
    globalThis.fetch = async () => new Response('Unauthorized', { status: 401 })

    let caught: unknown
    try {
      await new Publisher(config).publish('topic', {})
    } catch (err) {
      caught = err
    }

    assert.instanceOf(caught, MercurePublishError)
    assert.equal((caught as MercurePublishError).statusCode, 401)
  })

  test('throws MercureTimeoutError when request times out', async ({ assert }) => {
    globalThis.fetch = async () => {
      const err = new Error('The operation was aborted')
      err.name = 'AbortError'
      throw err
    }

    let caught: unknown
    try {
      await new Publisher(config).publish('topic', {})
    } catch (err) {
      caught = err
    }

    assert.instanceOf(caught, MercureTimeoutError)
    assert.equal((caught as MercureTimeoutError).timeoutMs, 5000)
  })

  test('wraps network failures in MercureConnectionError and keeps the cause', async ({
    assert,
  }) => {
    const reason = Object.assign(new Error('connect ECONNREFUSED 127.0.0.1:3000'), {
      code: 'ECONNREFUSED',
    })
    const original = new TypeError('fetch failed', { cause: reason })
    globalThis.fetch = async () => {
      throw original
    }

    let caught: unknown
    try {
      await new Publisher(config).publish('topic', {})
    } catch (err) {
      caught = err
    }

    assert.instanceOf(caught, MercureConnectionError)
    assert.instanceOf(caught, MercureError)
    assert.include((caught as Error).message, 'ECONNREFUSED')
    assert.strictEqual((caught as Error).cause, original)
  })

  test('handles multiple topics', async ({ assert }) => {
    let capturedBody = ''

    globalThis.fetch = async (_url, init) => {
      capturedBody = (init as RequestInit).body as string
      return new Response('1', { status: 200 })
    }

    await new Publisher(config).publish(['/a', '/b'], {})

    // URLSearchParams.getAll handles repeated keys
    const body = new URLSearchParams(capturedBody)
    assert.deepEqual(body.getAll('topic'), ['/a', '/b'])
  })
})

const modernConfig = {
  protocol: '1.x' as const,
  endpoint: config.endpoint,
  issuer: 'https://app.example.com',
  jwt: config.jwt,
}

test.group('Publisher with protocol 1.x', (group) => {
  let originalFetch: typeof globalThis.fetch
  let originalNow: typeof Date.now
  let tokens: string[]

  group.each.setup(() => {
    originalFetch = globalThis.fetch
    originalNow = Date.now
    tokens = []
    globalThis.fetch = async (_url, init) => {
      const headers = (init as RequestInit).headers as Record<string, string>
      tokens.push(headers.Authorization.replace('Bearer ', ''))
      return new Response('1', { status: 200 })
    }
  })

  group.each.teardown(() => {
    globalThis.fetch = originalFetch
    Date.now = originalNow
  })

  test('uses the configured adminToken as is', async ({ assert }) => {
    await new Publisher({ ...modernConfig, adminToken: 'my-token' }).publish('topic')

    assert.deepEqual(tokens, ['my-token'])
  })

  test('signs a short-lived publisher token', async ({ assert }) => {
    await new Publisher(modernConfig).publish('topic')

    const claims = JSON.parse(Buffer.from(tokens[0].split('.')[1], 'base64url').toString())

    assert.isTrue(jws.verify(tokens[0], 'HS256', modernConfig.jwt.secret))
    assert.equal(claims.sub, modernConfig.issuer)
    assert.equal(claims.exp, claims.iat + 300)
    assert.deepEqual(claims.authorization_details[0].actions, ['publish'])
    assert.deepEqual(claims.authorization_details[0].topics, [{ match: '*' }])
  })

  test('signs with publisherJwt when provided', async ({ assert }) => {
    const publisherJwt = { alg: 'HS512' as const, secret: 'publisher-secret' }
    await new Publisher({ ...modernConfig, publisherJwt }).publish('topic')

    assert.isTrue(jws.verify(tokens[0], 'HS512', publisherJwt.secret))
  })

  test('reuses the token then renews it before it expires', async ({ assert }) => {
    let now = originalNow()
    Date.now = () => now
    const publisher = new Publisher(modernConfig)

    await publisher.publish('topic')
    now += 239_000
    await publisher.publish('topic')
    now += 1000
    await publisher.publish('topic')

    assert.equal(tokens[1], tokens[0])
    assert.notEqual(tokens[2], tokens[0])
  })
})
