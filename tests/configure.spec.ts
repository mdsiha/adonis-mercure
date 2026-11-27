import { test } from '@japa/runner'
import { configure } from '../configure.js'
import { stubsRoot } from '../stubs/main.js'

function makeCommand() {
  const calls: { method: string; args: any[] }[] = []
  const record =
    (method: string) =>
    async (...args: any[]) => {
      calls.push({ method, args })
    }

  const codemods = {
    makeUsingStub: record('makeUsingStub'),
    defineEnvVariables: record('defineEnvVariables'),
    defineEnvValidations: record('defineEnvValidations'),
    updateRcFile: async (callback: (rcFile: any) => void) => {
      const providers: string[] = []
      callback({ addProvider: (path: string) => providers.push(path) })
      calls.push({ method: 'updateRcFile', args: providers })
    },
  }

  return { calls, command: { createCodemods: async () => codemods } as any }
}

test.group('configure', () => {
  test('creates config/mercure.ts from the stub', async ({ assert }) => {
    const { calls, command } = makeCommand()
    await configure(command)

    const call = calls.find((c) => c.method === 'makeUsingStub')
    assert.deepEqual(call?.args, [stubsRoot, 'config/mercure.stub', {}])
  })

  test('defines the env variables and their validation', async ({ assert }) => {
    const { calls, command } = makeCommand()
    await configure(command)

    const keys = ['MERCURE_ENDPOINT', 'MERCURE_ISSUER', 'MERCURE_JWT_SECRET']
    const vars = calls.find((c) => c.method === 'defineEnvVariables')
    const validations = calls.find((c) => c.method === 'defineEnvValidations')

    assert.deepEqual(Object.keys(vars!.args[0]), keys)
    assert.deepEqual(Object.keys(validations!.args[0].variables), keys)
  })

  test('accepts the localhost endpoint it writes to .env', async ({ assert }) => {
    const { calls, command } = makeCommand()
    await configure(command)

    const vars = calls.find((c) => c.method === 'defineEnvVariables')
    const validations = calls.find((c) => c.method === 'defineEnvValidations')

    assert.equal(new URL(vars!.args[0].MERCURE_ENDPOINT).hostname, 'localhost')
    assert.include(validations!.args[0].variables.MERCURE_ENDPOINT, 'tld: false')
  })

  test('writes the default issuer trusted by the hub', async ({ assert }) => {
    const { calls, command } = makeCommand()
    await configure(command)

    const vars = calls.find((c) => c.method === 'defineEnvVariables')

    assert.equal(vars!.args[0].MERCURE_ISSUER, 'https://localhost')
  })

  test('registers the provider in adonisrc.ts', async ({ assert }) => {
    const { calls, command } = makeCommand()
    await configure(command)

    const call = calls.find((c) => c.method === 'updateRcFile')
    assert.deepEqual(call?.args, ['@mdsiha369/adonis-mercure/mercure_provider'])
  })
})
