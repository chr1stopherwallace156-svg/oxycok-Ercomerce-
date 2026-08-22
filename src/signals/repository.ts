import {
  db
} from "../db/client.js";

import {
  signals
} from "../db/intelligence-schema.js";

import type {
  Signal
} from "./types.js";

export async function insertSignal(
  signal: Signal
) {
  await db
    .insert(signals)
    .values({
      signalId:
        signal.signalId,

      sourceId:
        signal.sourceId,

      sourceEventId:
        signal.sourceEventId,

      signalType:
        signal.signalType,

      entityType:
        signal.entityType,

      entityId:
        signal.entityId,

      metricName:
        signal.metricName,

      numericValue:
        signal.numericValue,

      textValue:
        signal.textValue,

      geography:
        signal.geography,

      authority:
        signal.authority,

      confidence:
        signal.confidence,

      observedAt:
        signal.observedAt,

      expiresAt:
        signal.expiresAt,

      metadata:
        signal.metadata
    })
    .onConflictDoNothing();
}