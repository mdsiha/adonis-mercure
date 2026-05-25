# Changelog

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

## [1.0.12] - 2025-08-01

Initial stable release.
