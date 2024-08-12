import { Mercure } from '../mercure.js'

declare module '@adonisjs/core/types' {
  export interface ContainerBindings {
    mercure: Mercure
  }
}
