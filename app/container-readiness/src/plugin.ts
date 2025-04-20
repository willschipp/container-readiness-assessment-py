import {
  createApiFactory,
  createPlugin,
  createRoutableExtension,
  discoveryApiRef,
  fetchApiRef,
} from '@backstage/core-plugin-api';
import { OrderApiRef, OrderApiClient } from './api';

import { rootRouteRef } from './routes';

export const containerReadinessPlugin = createPlugin({
  id: 'container-readiness',
  routes: {
    root: rootRouteRef,
  },
  apis: [
    createApiFactory({
      api: OrderApiRef,
      deps: {
        discoveryApi: discoveryApiRef,
        fetchApi: fetchApiRef,
      },
      factory: ({ discoveryApi, fetchApi}) => new OrderApiClient({discoveryApi, fetchApi}),
    }),
  ],
});

export const ContainerReadinessPage = containerReadinessPlugin.provide(
  createRoutableExtension({
    name: 'ContainerReadinessPage',
    component: () =>
      import('./components/HomeComponent').then(m => m.HomeComponent),
    mountPoint: rootRouteRef,
  }),
);
