export class ConnectorRateLimiter {
  private nextAllowedAt = 0;

  constructor(
    private readonly minimumIntervalMs:
      number
  ) {}

  async wait(): Promise<void> {
    const now = Date.now();

    const delay =
      this.nextAllowedAt -
      now;

    if (delay > 0) {
      await new Promise(
        resolve =>
          setTimeout(
            resolve,
            delay
          )
      );
    }

    this.nextAllowedAt =
      Date.now() +
      this.minimumIntervalMs;
  }

  deferFor(
    retryAfterMs: number
  ): void {
    this.nextAllowedAt =
      Math.max(
        this.nextAllowedAt,
        Date.now() +
          retryAfterMs
      );
  }
}