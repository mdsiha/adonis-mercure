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

const modernConfig = {
  protocol: '1.x' as const,
  endpoint: config.endpoint,
  issuer: 'https://app.example.com',
  jwt: config.jwt,
}

const DETAIL_TYPE = 'https://mercure.rocks/authorization-detail'

function decodeHeader(token: string) {
  return JSON.parse(Buffer.from(token.split('.')[0], 'base64url').toString())
}

test.group('TokenGenerator with protocol 1.x', () => {
  test('sets the at+jwt type in the header', async ({ assert }) => {
    const token = await new TokenGenerator(modernConfig).generateSubscribeToken(['/orders/42'])

    assert.deepEqual(decodeHeader(token), { alg: 'HS256', typ: 'at+jwt' })
  })

  test('sets the access token claims', async ({ assert }) => {
    const token = await new TokenGenerator(modernConfig).generateSubscribeToken(['/orders/42'])
    const claims = decode(token)

    assert.equal(claims.iss, modernConfig.issuer)
    assert.equal(claims.client_id, modernConfig.issuer)
    assert.equal(claims.aud, modernConfig.endpoint)
    assert.match(claims.sub, /^urn:uuid:/)
    assert.match(claims.jti, /^urn:uuid:/)
    assert.equal(claims.exp, claims.iat + 3600)
    assert.isUndefined(claims.mercure)
  })

  test('accepts a custom audience, subject and lifetime', async ({ assert }) => {
    const audience = ['http://mercure/.well-known/mercure', modernConfig.endpoint]
    const generator = new TokenGenerator({ ...modernConfig, audience })
    const token = await generator.generateSubscribeToken(['/orders/42'], {
      subject: 'user-1',
      expiresIn: 60,
    })
    const claims = decode(token)

    assert.deepEqual(claims.aud, audience)
    assert.equal(claims.sub, 'user-1')
    assert.equal(claims.exp, claims.iat + 60)
  })

  test('translates publish, subscribe and payload', async ({ assert }) => {
    const token = await new TokenGenerator(modernConfig).generate({
      publish: ['*'],
      subscribe: [
        { match: '/orders/:id', matchType: 'urlpattern' },
        { match: '/raw/{id}', matchType: 'exact' },
      ],
      payload: { user: 1 },
    })

    assert.deepEqual(decode(token).authorization_details, [
      { type: DETAIL_TYPE, actions: ['publish'], topics: [{ match: '*' }] },
      {
        type: DETAIL_TYPE,
        actions: ['subscribe'],
        topics: [{ match: '/orders/:id', match_type: 'urlpattern' }, { match: '/raw/{id}' }],
        payload: { user: 1 },
      },
    ])
  })

  test('grants nothing for an empty topic list', async ({ assert }) => {
    const token = await new TokenGenerator(modernConfig).generateSubscribeToken([])

    assert.deepEqual(decode(token).authorization_details, [])
  })

  test('rejects an unknown key', async ({ assert }) => {
    const generator = new TokenGenerator(modernConfig)

    await assert.rejects(() => generator.generate({ subscribes: ['*'] }), /Unknown key/)
  })

  test('rejects a URI template', async ({ assert }) => {
    const generator = new TokenGenerator(modernConfig)

    await assert.rejects(
      () => generator.generateSubscribeToken(['/orders/{id}']),
      /URI templates are not supported/
    )
  })

  test('rejects an invalid topic', async ({ assert }) => {
    const generator = new TokenGenerator(modernConfig)

    for (const topic of [42, null, { match: '/a' }, { match: '/a', matchType: 'regex' }]) {
      await assert.rejects(
        () => generator.generate({ subscribe: [topic] }),
        /A topic must be a string/
      )
    }
  })

  test('rejects a topic list that is not an array', async ({ assert }) => {
    const generator = new TokenGenerator(modernConfig)

    await assert.rejects(() => generator.generate({ publish: '*' }), /must be an array/)
  })

  test('rejects a payload without subscribe topic', async ({ assert }) => {
    const generator = new TokenGenerator(modernConfig)

    await assert.rejects(
      () => generator.generate({ publish: ['*'], payload: {} }),
      /payload requires/
    )
  })

  test('rejects topic matcher objects with protocol 0.x', async ({ assert }) => {
    const generator = new TokenGenerator(config)

    await assert.rejects(
      () => generator.generateSubscribeToken([{ match: '/a', matchType: 'exact' }]),
      /require protocol '1.x'/
    )
  })
})
