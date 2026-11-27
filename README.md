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
  AdonisJS v6 / v7 package to publish real-time updates via a <a href="https://mercure.rocks">Mercure Hub</a> (SSE)
</p>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Requirements](#requirements)
- [Hub compatibility](#hub-compatibility)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Mercure 1.x](#mercure-1x)
  - [Mercure 0.x](#mercure-0x)
  - [Upgrade from 0.x to 1.x](#upgrade-from-0x-to-1x)
- [Usage](#usage)
  - [Publish an update](#publish-an-update)
  - [Multiple topics](#multiple-topics)
  - [Private updates](#private-updates)
  - [SSE options (id, type, retry)](#sse-options-id-type-retry)
  - [Generate a subscriber token](#generate-a-subscriber-token)
  - [Health check](#health-check)
- [Testing](#testing)
- [API Reference](#api-reference)
  - [`send(topics, data?, options?)`](#sendtopics-data-options)
  - [`generateSubscribeToken(topics, options?)`](#generatesubscribetokentopics-options)
  - [`generate(payload, options?)`](#generatepayload-options)
  - [`ping()`](#ping)
- [Roadmap](#roadmap)
- [License](#license)

---

## Requirements

- AdonisJS **v6** or **v7**
- Node.js **>= 20.6.0**
- A running [Mercure Hub](https://mercure.rocks/docs/hub/install), 0.x or 1.x (see [Hub compatibility](#hub-compatibility))

## Hub compatibility

Mercure 1.x expects a new token format, so tell the package which one to sign with the `protocol` option. It is tested with `dunglas/mercure:v0.24` and `dunglas/mercure:v1.1.6`.

| Hub | `protocol`                 | Hub setting                                                          |
| --- | -------------------------- | -------------------------------------------------------------------- |
| 0.x | `'0.x'` (default)          | none                                                                 |
| 1.x | `'1.x'`                    | `MERCURE_TRUSTED_ISSUERS` must contain your `issuer`                 |
| 1.x | `'0.x'`, during migrations | `MERCURE_EXTRA_DIRECTIVES=protocol_version_compatibility 8` (legacy) |

A 1.x hub in normal mode rejects 0.x tokens with `401`.

## Installation

```bash
npm install @mdsiha369/adonis-mercure
node ace configure @mdsiha369/adonis-mercure
```

## Configuration

After running `ace configure`, a `config/mercure.ts` file is created and your `.env` is updated automatically. New installs use Mercure 1.x.

### Mercure 1.x

```ts
// config/mercure.ts
import env from '#start/env'
import { defineConfig } from '@mdsiha369/adonis-mercure'

export default defineConfig({
  protocol: '1.x',
  endpoint: env.get('MERCURE_ENDPOINT'),
  issuer: env.get('MERCURE_ISSUER'),
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

```env
MERCURE_ENDPOINT=http://localhost:3000/.well-known/mercure
MERCURE_ISSUER=https://localhost
MERCURE_JWT_SECRET=<your-jwt-secret>
```

| Option         | Required | Default    | Description                                                                |
| -------------- | -------- | ---------- | -------------------------------------------------------------------------- |
| `issuer`       | yes      | —          | `iss` claim of the tokens. The hub must trust it                           |
| `jwt`          | yes      | —          | Key signing subscriber tokens (`MERCURE_SUBSCRIBER_JWT_KEY` on the hub)    |
| `publisherJwt` | no       | `jwt`      | Key signing publisher tokens (`MERCURE_PUBLISHER_JWT_KEY` on the hub)      |
| `audience`     | no       | `endpoint` | `aud` claim, a string or an array                                          |
| `adminToken`   | no       | —          | Your own publisher token. Without it, the package signs short-lived tokens |

Set `publisherJwt` when your hub uses a different key for publishers.

**Audience.** The hub rejects a token whose `aud` is not its own URL. Unless `resource_identifier` is set on the hub, that URL is the one each client contacted. If your app publishes to `http://mercure/.well-known/mercure` while browsers subscribe to `https://hub.example.com/.well-known/mercure`, list both:

```ts
audience: [
  'http://mercure/.well-known/mercure',
  'https://hub.example.com/.well-known/mercure',
],
```

Behind a proxy that terminates TLS, configure `trusted_proxies` or `resource_identifier` on the hub, otherwise it expects an `http://` audience.

### Mercure 0.x

`protocol` can be omitted. Configurations written for previous versions of this package keep working.

```ts
export default defineConfig({
  endpoint: env.get('MERCURE_ENDPOINT'),
  adminToken: env.get('MERCURE_ADMIN_JWT'),
  jwt: {
    alg: 'HS256',
    secret: env.get('MERCURE_JWT_SECRET'),
  },
})
```

> **Note:** The `adminToken` must be a JWT signed with your hub's publisher key and a `"publish": ["*"]` claim in the `mercure` field.

### Upgrade from 0.x to 1.x

1. Upgrade the hub and set `MERCURE_TRUSTED_ISSUERS` to your issuer.
2. Add `protocol: '1.x'` and `issuer` to `config/mercure.ts`, remove `adminToken`, and add `MERCURE_ISSUER` to `.env` and `start/env.ts`.
3. Replace URI templates (`/orders/{id}`) with URL patterns: `{ match: '/orders/:id', matchType: 'urlpattern' }`.
4. In the browser, replace the `topic` query parameter with `match`, and rename the cookie to `__Secure-mercure_access_token`.
5. Stop passing the token in the URL (`?authorization=`), which 1.x no longer accepts.

See the [Mercure upgrade guide](https://github.com/dunglas/mercure/blob/v1.1.6/docs/UPGRADE.md) for the hub side.

---

## Usage

Import the service anywhere in your app:

```ts
import mercure from '@mdsiha369/adonis-mercure/services/main'
```

### Publish an update

```ts
const id = await mercure.send('/orders/42', { status: 'shipped' })
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

With 1.x, a string topic matches exactly. Use a matcher object for [URL patterns](https://developer.mozilla.org/en-US/docs/Web/API/URL_Pattern_API):

```ts
const token = await mercure.generateSubscribeToken([
  { match: '/orders/:id', matchType: 'urlpattern' },
])
```

`expiresIn` (in seconds) sets how long a token stays valid. With 1.x it defaults to `3600`. With 0.x, tokens do not expire by default.

```ts
const token = await mercure.generateSubscribeToken(['/orders/42'], { expiresIn: 600 })
```

With 1.x, the hub closes the connection when the token expires, and `EventSource` may stop retrying. Send a fresh token before that and open a new `EventSource` if needed.

Browsers cannot send an `Authorization` header with `EventSource`, so there are two ways to give the token to the hub.

**Option 1: cookie (works with a plain `EventSource`)**

Set the token in a cookie from your AdonisJS app. Use `plainCookie` with
`encode: false`. `response.cookie` signs the value, and `plainCookie` encodes it
in base64 by default: in both cases the hub cannot read the token and answers `401`.

```ts
router.get('/orders/:id/subscribe', async ({ params, response }) => {
  const token = await mercure.generateSubscribeToken([`/orders/${params.id}`])

  // 0.x hubs: name the cookie 'mercureAuthorization'
  response.plainCookie('__Secure-mercure_access_token', token, {
    encode: false,
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
  })

  return { ok: true }
})
```

Then, in the browser:

```ts
const url = new URL('https://hub.example.com/.well-known/mercure')
url.searchParams.append('match', '/orders/42') // 0.x hubs: 'topic'

const eventSource = new EventSource(url, { withCredentials: true })
```

- These are the default cookie names. If you changed the `cookie_name` setting of your hub, use that name instead.
- The app and the hub must share the same registrable domain (for example `app.example.com` and `hub.example.com`). Add `domain: '.example.com'` to the cookie options in that case.
- `secure: true` requires HTTPS, and browsers refuse a `__Secure-` cookie without it. For local HTTP development, use `secure: false` and, with 1.x, a name without the prefix set in `cookie_name` on the hub.
- If your app and your hub have different origins (another subdomain or port), add the origin of your app to the `cors_origins` directive of the hub.

**Option 2: `Authorization` header**

Use a client that reads the stream with `fetch()`, such as `@microsoft/fetch-event-source`:

```ts
import { fetchEventSource } from '@microsoft/fetch-event-source'

await fetchEventSource(url.toString(), {
  headers: { Authorization: `Bearer ${token}` },
  onmessage(event) {
    console.log(event.data)
  },
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

// assert an exact number of messages
fake.assertSentCount(2)

// inspect all recorded messages
const messages = fake.getSent()

// inspect the payloads passed to generate() / generateSubscribeToken()
const tokens = fake.getTokens()

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

Returns the id of the published update. The hub generates one (`urn:uuid:...`) unless you pass `id` in the options.

Throws `MercurePublishError` if the hub returns a non-2xx response.  
Throws `MercureTimeoutError` if the hub does not respond within the configured timeout.  
Throws `MercureConnectionError` if the hub cannot be reached (connection refused, DNS failure, ...). The original error is available in `error.cause`.

---

### `generateSubscribeToken(topics, options?)`

Generates a JWT allowing a frontend client to subscribe to `topics`. A topic is a string or, with 1.x, a `{ match, matchType }` object where `matchType` is `'exact'` or `'urlpattern'`.

```ts
const token = await mercure.generateSubscribeToken(['/chat/1', '/notifications/me'])
```

The `*` topic grants access to every private update: don't pass user input directly.

**`TokenOptions`**

| Property    | Type     | Description                                                              |
| ----------- | -------- | ------------------------------------------------------------------------ |
| `expiresIn` | `number` | Lifetime in seconds. Default: `3600` with 1.x, no expiration with 0.x    |
| `subject`   | `string` | `sub` claim, 1.x only. A random `urn:uuid:` is used when it is not given |

---

### `generate(payload, options?)`

Low-level JWT generation. With 0.x, `payload` is wrapped under the `mercure` claim. With 1.x, it is translated to the `authorization_details` claim and only accepts the `subscribe`, `publish` and `payload` keys.

```ts
const token = await mercure.generate({
  subscribe: ['/chat/1'],
  publish: ['/chat/1'],
  payload: { room: 1 },
})
```

With 1.x, `payload` is attached to the subscribe grant. The hub shares it with other authorized subscribers, so don't put secrets in it. Takes the same options as `generateSubscribeToken`.

---

### `ping()`

Returns `true` if the hub answers, including with a 4xx status. Returns `false` if the hub answers with a 5xx status, if the request fails, or if it times out.

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
