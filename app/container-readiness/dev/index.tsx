import { createDevApp } from '@backstage/dev-utils';
import { containerReadinessPlugin, ContainerReadinessPage } from '../src/plugin';

createDevApp()
  .registerPlugin(containerReadinessPlugin)
  .addPage({
    element: <ContainerReadinessPage />,
    title: 'Root Page',
    path: '/container-readiness',
  })
  .render();
