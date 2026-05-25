import { test } from '@japa/runner'
import { FakeMercure } from '../src/fake_mercure.js'

test.group('FakeMercure', () => {
  test('records sent messages', async ({ assert }) => {
    const fake = new FakeMercure()
    await fake.send('/orders/1', { status: 'shipped' })

    const sent = fake.getSent()
    assert.lengthOf(sent, 1)
    assert.deepEqual(sent[0].topics, ['/orders/1'])
    assert.deepEqual(sent[0].data, { status: 'shipped' })
  })

  test('assertSent passes when topic matches', async ({ assert }) => {
    const fake = new FakeMercure()
    await fake.send('/topic', { foo: 'bar' })

    assert.doesNotThrow(() => fake.assertSent('/topic'))
  })

  test('assertSent passes when topic and data match', async ({ assert }) => {
    const fake = new FakeMercure()
    await fake.send('/topic', { foo: 'bar' })

    assert.doesNotThrow(() => fake.assertSent('/topic', { foo: 'bar' }))
  })

  test('assertSent throws when topic was not sent', ({ assert }) => {
    const fake = new FakeMercure()

    assert.throws(() => fake.assertSent('/missing'))
  })

  test('assertSent throws when data does not match', async ({ assert }) => {
    const fake = new FakeMercure()
    await fake.send('/topic', { foo: 'bar' })

    assert.throws(() => fake.assertSent('/topic', { foo: 'wrong' }))
  })

  test('assertNotSent passes when topic was never sent', ({ assert }) => {
    const fake = new FakeMercure()

    assert.doesNotThrow(() => fake.assertNotSent('/topic'))
  })

  test('assertNotSent throws when topic was sent', async ({ assert }) => {
    const fake = new FakeMercure()
    await fake.send('/topic', {})

    assert.throws(() => fake.assertNotSent('/topic'))
  })

  test('assertNothingSent passes on fresh instance', ({ assert }) => {
    const fake = new FakeMercure()

    assert.doesNotThrow(() => fake.assertNothingSent())
  })

  test('assertNothingSent throws after a send', async ({ assert }) => {
    const fake = new FakeMercure()
    await fake.send('/topic', {})

    assert.throws(() => fake.assertNothingSent())
  })

  test('clear resets all recorded messages', async ({ assert }) => {
    const fake = new FakeMercure()
    await fake.send('/topic', {})
    fake.clear()

    assert.lengthOf(fake.getSent(), 0)
    assert.doesNotThrow(() => fake.assertNothingSent())
  })

  test('handles boolean true as private option', async ({ assert }) => {
    const fake = new FakeMercure()
    await fake.send('/topic', {}, true)

    const sent = fake.getSent()
    assert.isTrue(sent[0].options.private)
  })

  test('ping always returns true', async ({ assert }) => {
    const fake = new FakeMercure()
    assert.isTrue(await fake.ping())
  })

  test('generate stores the payload and returns fake-token', async ({ assert }) => {
    const fake = new FakeMercure()
    const token = await fake.generate({ subscribe: ['/chat/1'] })

    assert.equal(token, 'fake-token')
  })

  test('generateSubscribeToken returns fake-token', async ({ assert }) => {
    const fake = new FakeMercure()
    const token = await fake.generateSubscribeToken(['/orders/42'])

    assert.equal(token, 'fake-token')
  })
})
