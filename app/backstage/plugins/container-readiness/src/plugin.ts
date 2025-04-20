import {
  createPlugin,
  createRoutableExtension,
} from '@backstage/core-plugin-api';

import { rootRouteRef } from './routes';

export const containerReadinessPlugin = createPlugin({
  id: 'container-readiness',
  routes: {
    root: rootRouteRef,
  },
});

export const ContainerReadinessPage = containerReadinessPlugin.provide(
  createRoutableExtension({
    name: 'ContainerReadinessPage',
    component: () =>
      import('./components/HomeComponent').then(m => m.HomeComponent),
    mountPoint: rootRouteRef,
  }),
);
