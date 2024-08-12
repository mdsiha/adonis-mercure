<p align="center">
  <a href="https://www.npmjs.com/package/@das3mical/adonis-mercure"><img src="https://img.shields.io/npm/dm/@das3mical/adonis-mercure.svg?style=flat-square" alt="Download"></a>
  <a href="https://www.npmjs.com/package/@das3mical/adonis-mercure"><img src="https://img.shields.io/npm/v/@das3mical/adonis-mercure.svg?style=flat-square" alt="Version"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/npm/l/@das3mical/adonis-mercure.svg?style=flat-square" alt="License"></a>
</p>

# @das3mical/adonis-mercure

`@das3mical/adonis-mercure` is a Mercure client for AdonisJS, enabling the use of Server-Sent Events (SSE) to push real-time updates to your clients over HTTP.

## Getting Started

### Prerequisites

To use this package, you must have a Mercure Hub instance running. The Mercure Hub is responsible for broadcasting the SSEs to clients.

### Installation

This package is available on the npm registry. Install it using the following command:

```bash
npm install @das3mical/adonis-mercure
```

Next, configure the package by running the configuration command:

```bash
node ace configure @das3mical/adonis-mercure
```

Your package is now configured.

### Configuration

Before using the package, you'll need to set up the configuration. The configuration is stored in the `config/mercure.ts` file.

Here are the key configuration options:

- **endpoint**: The endpoint of the Mercure Hub.
- **adminToken**: The JWT created to authenticate as an admin of the Mercure Hub.
- **jwt.alg**: The algorithm used to sign the JWT. This should match the configuration of your Mercure Hub.
- **jwt-secret**: The secret key used to sign the JWT. This must correspond with your Mercure Hub's configuration.

#### Admin Token Example

The \`**adminToken**\` must be generated using the same \`**alg**\` and \`**secret**\` as your Mercure Hub, with the following payload:

```json
{
  "mercure": {
    "publish": ["*"]
  }
}
```

For example, given the secret \`**ChangeMe**\` and the algorithm \`**HS256**\`, the JWT would be:

```
eyJhbGciOiJIUzI1NiJ9.eyJtZXJjdXJlIjp7InB1Ymxpc2giOlsiKiJdfX0.mx2ROlYlE1rp7udoDy-WCdnpLdPuKWzDxoBJXGMK4OE
```

### Usage

This package provides access to two main functions:

1. **generate**: Used to generate a JWT token for client authentication.
2. **send**: Used to publish updates to the Mercure Hub.

#### 1. Generating JWT Tokens

The \`**generate**\` function creates a JWT token for a given payload, which can be used for subscribing to private topics.

```ts
import mercure from '@das3mical/adonis-mercure'

const token = mercure.generate({
  subscribe: ['your-topic'], // example: subscribe: ['/chat/1'],
})
```

### Sending Updates

The \`**send**\` function allows you to send data to one or more topics. You can also mark events as private if needed.

The \`**send**\` method accepts three arguments:

- **topic**: The topic to which the update will be published.
- **data**: The data to be published.
- **isPrivate**: Indicates whether the update should be private.

For more details on the \`**topic**\` and \`**data**\` arguments, please refer to the [Mercure documentation](https://mercure.rocks/spec#publication).

```ts
import mercure from '@das3mical/adonis-mercure'

mercure.send('your-topic', {
  message: 'Hello, World!',
})
```

To send private events, set the \`**isPrivate**\` flag to \`**true**\`:

```ts
import mercure from '@das3mical/adonis-mercure'

mercure.send(
  'your-topic',
  {
    message: 'Private event',
  },
  true
)
```
