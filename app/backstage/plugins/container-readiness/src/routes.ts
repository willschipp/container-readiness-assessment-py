import { createRouteRef } from '@backstage/core-plugin-api';

export const rootRouteRef = createRouteRef({
  id: 'container-readiness',
});

export const orderRouteRef = createRouteRef({
  id: 'container-readiness-order',
  params: ['order_id']
});
