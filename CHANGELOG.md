# Changelog

## [2.0.0] - Unreleased

### Added

- `generateSubscribeToken(topics: string[])` — typed shorthand for subscriber JWT tokens
- `send()` now accepts an options object as third argument: `{ private, id, type, retry }`
- `ping()` — returns `true` if the Mercure Hub is reachable
- `FakeMercure` — test double with `assertSent()`, `assertNotSent()`, `assertNothingSent()`, `getSent()`, `clear()`
- `MercureContract` interface — implemented by both `Mercure` and `FakeMercure`
- `MercurePublishError` — thrown when the hub returns a non-2xx response (statusCode + responseBody)
- `MercureConfigError` — thrown at app boot when config is missing or incomplete
- Full test suite (Japa)

### Changed

- Internal architecture split into `TokenGenerator` and `Publisher` — smaller, focused classes
- `generate()` return type is now `Promise<string>` instead of `Promise<unknown>`
- `send()` data parameter type widened to `Record<string, unknown>` (was `Record<string, string>`)
- Replaced `got` HTTP client with native `fetch` — one fewer dependency
- Provider now throws `MercureConfigError` at boot instead of creating a broken instance
- Errors are thrown (not swallowed) when the hub returns a non-2xx status

### Removed

- `got` dependency

---

## [1.0.12] - 2025-08-01

Initial stable release.
