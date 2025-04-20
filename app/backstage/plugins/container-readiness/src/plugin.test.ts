import { containerReadinessPlugin } from './plugin';

describe('container-readiness', () => {
  it('should export plugin', () => {
    expect(containerReadinessPlugin).toBeDefined();
  });
});
