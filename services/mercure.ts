import app from '@adonisjs/core/services/app'
import { Mercure } from '../src/mercure.js'

let mercure: Mercure

await app.booted(async () => {
  mercure = await app.container.make('mercure')
})

export { mercure as default }
