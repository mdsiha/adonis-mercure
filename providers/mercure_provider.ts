import '../src/types/extended.js'
import { Mercure } from '../src/mercure.js'
import type { ApplicationService } from '@adonisjs/core/types'
import type { MercureConfig } from '../src/types/main.js'

export default class MercureProvider {
  constructor(protected app: ApplicationService) {}

  async boot() {
    this.app.container.singleton('mercure', async () => {
      const config = this.app.config.get<MercureConfig>('mercure', {})

      return new Mercure(config)
    })
  }
}
