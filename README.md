<p align="center">
  <img src="https://raw.githubusercontent.com/mdsiha/adonis-mercure/main/assets/logo.svg" width="100" alt="adonis-mercure" />
</p>

<h1 align="center">@mdsiha369/adonis-mercure</h1>

<p align="center">
  <a href="https://github.com/mdsiha/adonis-mercure/actions/workflows/test.yml"><img src="https://github.com/mdsiha/adonis-mercure/actions/workflows/test.yml/badge.svg" alt="Tests"></a>
  <a href="https://www.npmjs.com/package/@mdsiha369/adonis-mercure"><img src="https://img.shields.io/npm/dm/@mdsiha369/adonis-mercure.svg?style=flat-square" alt="Downloads"></a>
  <a href="https://www.npmjs.com/package/@mdsiha369/adonis-mercure"><img src="https://img.shields.io/npm/v/@mdsiha369/adonis-mercure.svg?style=flat-square" alt="Version"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/npm/l/@mdsiha369/adonis-mercure.svg?style=flat-square" alt="License"></a>
</p>

<p align="center">
  AdonisJS v6 package to publish real-time updates via a <a href="https://mercure.rocks">Mercure Hub</a> (SSE)
</p>

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Publish an update](#publish-an-update)
  - [Multiple topics](#multiple-topics)
  - [Private updates](#private-updates)
  - [SSE options](#sse-options-id-type-retry)
  - [Generate a subscriber token](#generate-a-subscriber-token)
  - [Health check](#health-check)
- [Testing](#testing)
- [API Reference](#api-reference)
- [Roadmap](#roadmap)
- [License](#license)

---

## Requirements

- AdonisJS **v6**
- Node.js **>= 20.6.0**
- A running [Mercure Hub](https://mercure.rocks/docs/hub/install)

## Installation

```bash
npm install @mdsiha369/adonis-mercure
node ace configure @mdsiha369/adonis-mercure
```

## Configuration

After running `ace configure`, a `config/mercure.ts` file is created and your `.env` is updated automatically.

```ts
// config/mercure.ts
import env from '#start/env'
import { defineConfig } from '@mdsiha369/adonis-mercure'

export default defineConfig({
  endpoint: env.get('MERCURE_ENDPOINT'),
  adminToken: env.get('MERCURE_ADMIN_JWT'),
  jwt: {
    alg: 'HS256',
    secret: env.get('MERCURE_JWT_SECRET'),
  },
  // optional — default: 5000ms, set to 0 to disable
  http: {
    timeout: 5000,
  },
})
```

Set the following env variables in your `.env`:

```env
MERCURE_ENDPOINT=http://localhost:3000/.well-known/mercure
MERCURE_ADMIN_JWT=<your-admin-jwt>
MERCURE_JWT_SECRET=<your-jwt-secret>
```

> **Note:** The `adminToken` must be a JWT signed with your hub's secret and a `"publish": ["*"]` claim in the `mercure` field. See the [Mercure auth docs](https://mercure.rocks/docs/hub/auth) for details.

---

## Usage

Import the service anywhere in your app:

```ts
import mercure from '@mdsiha369/adonis-mercure/services/main'
```

### Publish an update

```ts
await mercure.send('/orders/42', { status: 'shipped' })
```

### Multiple topics

```ts
await mercure.send(['/orders/42', '/notifications/user/1'], { status: 'shipped' })
```

### Private updates

Private updates are only delivered to authenticated subscribers who hold a valid token for that topic.

```ts
// shorthand (backward compatible)
await mercure.send('/orders/42', { status: 'shipped' }, true)

// options object
await mercure.send('/orders/42', { status: 'shipped' }, { private: true })
```

### SSE options (id, type, retry)

```ts
await mercure.send(
  '/orders/42',
  { status: 'shipped' },
  {
    id: 'msg-001', // event ID — enables reconnection recovery
    type: 'order.shipped', // event type
    retry: 5000, // client reconnect delay in ms
    private: true,
  }
)
```

### Generate a subscriber token

Use this to create JWT tokens for your frontend clients so they can subscribe to topics, including private ones.

```ts
// typed shorthand
const token = await mercure.generateSubscribeToken(['/orders/42'])

// or low-level
const token = await mercure.generate({ subscribe: ['/orders/42'] })
```

Pass the token to your frontend:

```ts
const url = new URL('http://localhost:3000/.well-known/mercure')
url.searchParams.append('topic', '/orders/42')

const eventSource = new EventSource(url.toString(), {
  headers: { Authorization: `Bearer ${token}` },
})
```

### Health check

```ts
const isReachable = await mercure.ping() // true | false
```

---

## Testing

`FakeMercure` lets you test your application code without a real Mercure Hub.

**Swap the container binding in your test setup:**

```ts
import { FakeMercure } from '@mdsiha369/adonis-mercure'

// before your test
app.container.swap('mercure', () => new FakeMercure())

// after your test
app.container.restore('mercure')
```

**Assert on what was sent:**

```ts
const fake = (await app.container.make('mercure')) as FakeMercure

// assert a topic received a message
fake.assertSent('/orders/42')

// assert a topic received a specific payload
fake.assertSent('/orders/42', { status: 'shipped' })

// assert a topic was never sent to
fake.assertNotSent('/admin/secret')

// assert nothing was sent at all
fake.assertNothingSent()

// inspect all recorded messages
const messages = fake.getSent()

// reset between tests
fake.clear()
```

---

## API Reference

### `send(topics, data?, options?)`

Publishes an update to the Mercure Hub.

| Parameter | Type                      | Default | Description                                            |
| --------- | ------------------------- | ------- | ------------------------------------------------------ |
| `topics`  | `string \| string[]`      | —       | Topic(s) to publish to                                 |
| `data`    | `Record<string, unknown>` | `{}`    | Payload — serialized as JSON                           |
| `options` | `boolean \| SendOptions`  | `false` | `true` for private (legacy), or a `SendOptions` object |

**`SendOptions`**

| Property  | Type      | Description                                    |
| --------- | --------- | ---------------------------------------------- |
| `private` | `boolean` | Restrict delivery to authenticated subscribers |
| `id`      | `string`  | SSE event ID (enables reconnection recovery)   |
| `type`    | `string`  | SSE event type                                 |
| `retry`   | `number`  | Client reconnect delay in milliseconds         |

Throws `MercurePublishError` if the hub returns a non-2xx response.  
Throws `MercureTimeoutError` if the hub does not respond within the configured timeout.

---

### `generateSubscribeToken(topics)`

Generates a JWT with `{ subscribe: topics }` for a frontend client.

```ts
const token = await mercure.generateSubscribeToken(['/chat/1', '/notifications/me'])
```

---

### `generate(payload)`

Low-level JWT generation. Wraps `payload` under the `mercure` claim.

```ts
const token = await mercure.generate({ subscribe: ['/chat/1'], publish: ['/chat/1'] })
```

---

### `ping()`

Returns `true` if the hub is reachable, `false` on network error or timeout.

---

## Roadmap

Features planned for upcoming releases:

- **`generatePublishToken(topics)`** — typed shorthand for publisher JWT tokens (symmetric to `generateSubscribeToken`)
- **`sendBatch(messages[])`** — publish multiple updates in a single call
- **Retry with backoff** — automatic retry on transient hub errors with configurable strategy
- **Typed event classes** — define reusable event objects (`new OrderShippedEvent(id)`) instead of inline payloads

Have a use case or suggestion? [Open an issue](https://github.com/mdsiha/adonis-mercure/issues).

---

## License

MIT — [Michael DAŞ](https://github.com/mdsiha)
