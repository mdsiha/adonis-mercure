/*
|--------------------------------------------------------------------------
| Configure hook
|--------------------------------------------------------------------------
|
| The configure hook is called when someone runs "node ace configure <package>"
| command. You are free to perform any operations inside this function to
| configure the package.
|
| To make things easier, you have access to the underlying "ConfigureCommand"
| instance and you can use codemods to modify the source files.
|
*/

import ConfigureCommand from '@adonisjs/core/commands/configure'
import { stubsRoot } from './stubs/main.js'

export async function configure(_command: ConfigureCommand) {
  const codemods = await _command.createCodemods()

  await codemods.makeUsingStub(stubsRoot, 'config/mercure.stub', {})

  await codemods.defineEnvVariables({
    MERCURE_ENDPOINT: 'http://localhost:3333/.well-known/mercure',
    MERCURE_ADMIN_JWT:
      'eyJhbGciOiJIUzI1NiJ9.eyJtZXJjdXJlIjp7InB1Ymxpc2giOlsiKiJdfX0.mx2ROlYlE1rp7udoDy-WCdnpLdPuKWzDxoBJXGMK4OE',
    MERCURE_JWT_SECRET: 'ChangeMe',
  })

  await codemods.defineEnvValidations({
    variables: {
      MERCURE_ENDPOINT: `Env.schema.string({ format: 'url' })`,
      MERCURE_ADMIN_JWT: `Env.schema.string()`,
      MERCURE_JWT_SECRET: `Env.schema.string()`,
    },
    leadingComment: 'Mercure configuration',
  })

  await codemods.updateRcFile((rcFile) => {
    rcFile.addProvider('@das3mical/adonis-mercure/mercure_provider')
  })
}
