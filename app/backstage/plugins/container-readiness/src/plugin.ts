import {
  createApiFactory,
  createPlugin,
  createRoutableExtension,
  discoveryApiRef,
  fetchApiRef,
} from '@backstage/core-plugin-api';
import { OrderApiRef, OrderApiClient } from './api';
import { orderRouteRef, rootRouteRef } from './routes';


export const containerReadinessPlugin = createPlugin({
  id: 'container-readiness',
  routes: {
    root: rootRouteRef,
    order: orderRouteRef,
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

export const ContainerReadinessOrderPage = containerReadinessPlugin.provide(
  createRoutableExtension({
    name: 'ContainerReadinessOrderPage',
    component: () =>
      import('./components/OrderComponent').then(m => m.OrderComponent),
    mountPoint: orderRouteRef,
  }),
);
