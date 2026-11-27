import '../src/types/extended.js'
import { Mercure } from '../src/mercure.js'
import { MercureConfigError } from '../src/errors/config_error.js'
import type { ApplicationService } from '@adonisjs/core/types'
import type { MercureConfig } from '../src/types/main.js'

export default class MercureProvider {
  constructor(protected app: ApplicationService) {}

  async boot() {
    this.app.container.singleton('mercure', async () => {
      const config = this.app.config.get<MercureConfig | undefined>('mercure')

      const missingCredential = config?.protocol === '1.x' ? !config.issuer : !config?.adminToken

      if (!config?.endpoint || !config.jwt?.secret || missingCredential) {
        throw new MercureConfigError(
          'Missing or incomplete Mercure config. Run "node ace configure @mdsiha369/adonis-mercure"'
        )
      }

      return new Mercure(config)
    })
  }
}
