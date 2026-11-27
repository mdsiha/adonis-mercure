# Changelog

## [Unreleased]

### Added

- Mercure 1.x support with the new `protocol: '1.x'` option: RFC 9068 access tokens with `authorization_details`, and the `issuer`, `audience` and `publisherJwt` options
- In 1.x, `adminToken` is optional: the package signs and renews its own publisher token
- `{ match, matchType }` topics and the `subject` token option, both for 1.x
- Public types `TopicMatcher`, `JwtConfig`, `LegacyMercureConfig` and `ModernMercureConfig`
- README: configuration and upgrade guide for Mercure 1.x

### Changed

- `node ace configure` now generates a Mercure 1.x configuration with `MERCURE_ISSUER` instead of `MERCURE_ADMIN_JWT`. Existing apps are not affected and keep using 0.x
- `MercureConfig` is now a union type: an interface can no longer extend it
- `defineConfig()` rejects an unknown `protocol`

### Removed

- README: the "Performance" section, as the scripts behind its numbers are not part of the repository

---

## [3.0.1] - 2026-11-25

### Fixed

- `node ace configure` generated an env validation that rejected the default `http://localhost:3000` endpoint. `MERCURE_ENDPOINT` is now validated with `tld: false`. Existing apps must add this option to `start/env.ts` themselves
- README: the cookie example did not work. `plainCookie` needs `encode: false`, and Mercure 0.x hubs read the `mercureAuthorization` cookie

### Added

- README: "Hub compatibility" and "Performance" sections, and a note about `cors_origins`

---

## [3.0.0] - 2026-11-16

### Changed

- **Breaking:** `send()` now returns the id of the published update as a string instead of a `Response`. The hub generates a `urn:uuid:...` id unless you pass `id` in the options. Code that read the response (`response.status`, `await response.text()`) must use the returned id instead. Classes implementing `MercureContract` must change the return type of `send()` to `Promise<string>`

---

## [2.2.0] - 2026-11-15

### Added

- `MercureConnectionError`, thrown by `send()` when the hub cannot be reached. It extends `MercureError` and keeps the original error in `cause`
- `expiresIn` option (in seconds) on `generate()` and `generateSubscribeToken()` to set the JWT `exp` claim. Tokens still do not expire when it is omitted
- Tests for `defineConfig()`, the provider and the `configure` hook
- `FakeMercure.assertSentCount()` and `FakeMercure.getTokens()`
- Public types (`MercureConfig`, `MercureContract`, `SendOptions`, `TokenOptions`, `JwtAlgorithm`, `SentMessage`) can now be imported from the package root. The `/types` subpath still works

### Fixed

- Published types no longer depend on `@types/jws`: `jwt.alg` is now typed with the new `JwtAlgorithm` union instead of `any` in user projects
- README: the browser subscription example did not work (`EventSource` cannot send an `Authorization` header). It now documents the cookie and fetch options
- `ping()` now returns `false` when the hub answers with a 5xx status instead of reporting it as reachable
- `FakeMercure.assertSent()` no longer fails when the expected data has its keys in a different order

### Changed

- `send()` no longer throws the raw `fetch` error (`TypeError: fetch failed`) on network failures. Code that catches that `TypeError` should catch `MercureConnectionError` instead
- The npm package no longer ships the compiled tests or the raw `.ts` sources (13.7 kB down to 9.0 kB)
- `defineConfig()` now rejects an `endpoint` that is not an http(s) URL and an empty `adminToken`, so misconfiguration fails at startup
- AdonisJS v7 is now accepted by the `@adonisjs/core` peer dependency range, and CI runs the typecheck and tests against it

---

## [2.1.2] - 2026-05-25

### Changed

- Package renamed from `@das3mical/adonis-mercure` to `@mdsiha369/adonis-mercure`. The old package is deprecated and will not receive updates. To migrate, install the new package and replace the old name in `adonisrc.ts`, `config/mercure.ts` and your imports

---

## [2.1.1] - 2026-05-25

### Changed

- Updated package description and keywords for better discoverability on npm and search engines

---

## [2.1.0] - 2026-05-25

### Added

- Configurable HTTP timeout for `send()` and `ping()` via `http.timeout` in config (default: 5000ms, 0 to disable)
- `MercureTimeoutError` — thrown when the hub does not respond within the configured timeout

---

## [2.0.1] - 2026-05-25

### Fixed

- Removed hardcoded admin JWT and `ChangeMe` secret from `configure.ts` — empty values now force developers to set proper credentials before the app starts
- `defineConfig` now rejects the `none` algorithm and any algorithm outside the allowed list (HS256/384/512, RS256/384/512)
- `defineConfig` now requires `jwt.secret` to be at least 32 characters long
- `MercurePublishError.responseBody` is truncated to 200 characters to limit sensitive data exposure in logs

---

## [2.0.0] - 2026-05-25

### Added

- `generateSubscribeToken(topics: string[])` — typed shorthand for subscriber JWT tokens
- `send()` now accepts an options object as third argument: `{ private, id, type, retry }`
- `ping()` — returns `true` if the Mercure Hub is reachable
- `FakeMercure` — test double with `assertSent()`, `assertNotSent()`, `assertNothingSent()`, `getSent()`, `clear()`
- `MercureContract` interface — implemented by both `Mercure` and `FakeMercure`
- `MercurePublishError` — thrown when the hub returns a non-2xx response
- `MercureConfigError` — thrown at app boot when config is missing or incomplete
- Full test suite (Japa)

### Changed

- Internal architecture split into `TokenGenerator` and `Publisher`
- `generate()` return type is now `Promise<string>` instead of `Promise<unknown>`
- `send()` data parameter type widened to `Record<string, unknown>` (was `Record<string, string>`)
- Replaced `got` HTTP client with native `fetch`
- Provider now throws `MercureConfigError` at boot instead of creating a broken instance
- Errors are thrown instead of swallowed when the hub returns a non-2xx status

### Removed

- `got` dependency

---

## [1.0.12] - 2024-08-12

Initial stable release.
