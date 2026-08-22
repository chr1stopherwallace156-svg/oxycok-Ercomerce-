import {
  boolean,
  doublePrecision,
  index,
  integer,
  jsonb,
  pgEnum,
  pgTable,
  text,
  timestamp,
  uniqueIndex,
  uuid
} from "drizzle-orm/pg-core";

import {
  commerceEvents,
  sources
} from "./schema.js";

/**
 * SIGNALS
 *
 * A signal is a normalized observation derived from
 * one or more source events.
 *
 * Signals are evidence.
 * They are NOT hypotheses and NOT decisions.
 */

export const signalAuthorityEnum =
  pgEnum("signal_authority", [
    "TRANSACTIONAL_TRUTH",
    "FIRST_PARTY_BEHAVIOR",
    "EXTERNAL_CONTEXT",
    "RESEARCH_EVIDENCE",
    "DERIVED_ANALYSIS"
  ]);

export const signals = pgTable(
  "signals",
  {
    id: uuid("id")
      .defaultRandom()
      .primaryKey(),

    signalId: text("signal_id")
      .notNull(),

    sourceId: text("source_id")
      .notNull()
      .references(() => sources.id),

    sourceEventId: text(
      "source_event_id"
    ),

    signalType: text(
      "signal_type"
    ).notNull(),

    entityType: text(
      "entity_type"
    ).notNull(),

    entityId: text(
      "entity_id"
    ).notNull(),

    metricName: text(
      "metric_name"
    ).notNull(),

    numericValue:
      doublePrecision(
        "numeric_value"
      ),

    textValue: text(
      "text_value"
    ),

    geography: text(
      "geography"
    ),

    authority:
      signalAuthorityEnum(
        "authority"
      ).notNull(),

    confidence:
      doublePrecision(
        "confidence"
      ),

    observedAt:
      timestamp(
        "observed_at",
        {
          withTimezone: true
        }
      ).notNull(),

    expiresAt:
      timestamp(
        "expires_at",
        {
          withTimezone: true
        }
      ),

    metadata:
      jsonb("metadata")
        .notNull()
        .default({}),

    createdAt:
      timestamp(
        "created_at",
        {
          withTimezone: true
        }
      )
        .notNull()
        .defaultNow()
  },
  (table) => ({
    signalUnique:
      uniqueIndex(
        "signals_signal_id_unique"
      ).on(table.signalId),

    entityIndex:
      index(
        "signals_entity_idx"
      ).on(
        table.entityType,
        table.entityId
      ),

    metricIndex:
      index(
        "signals_metric_idx"
      ).on(
        table.metricName
      ),

    observedIndex:
      index(
        "signals_observed_idx"
      ).on(
        table.observedAt
      )
  })
);

/**
 * SIGNAL PROVENANCE
 *
 * One signal may depend on multiple events.
 * Do not hide that lineage inside JSON.
 */

export const signalEvidence =
  pgTable(
    "signal_evidence",
    {
      id: uuid("id")
        .defaultRandom()
        .primaryKey(),

      signalId: text(
        "signal_id"
      ).notNull(),

      commerceEventId:
        uuid(
          "commerce_event_id"
        )
          .notNull()
          .references(
            () =>
              commerceEvents.id
          ),

      role: text(
        "role"
      )
        .notNull()
        .default(
          "SOURCE_EVENT"
        ),

      createdAt:
        timestamp(
          "created_at",
          {
            withTimezone: true
          }
        )
          .notNull()
          .defaultNow()
    },
    (table) => ({
      sourceBinding:
        uniqueIndex(
          "signal_evidence_unique"
        ).on(
          table.signalId,
          table.commerceEventId,
          table.role
        )
    })
  );

/**
 * FEATURE DEFINITIONS
 *
 * Definitions are durable.
 * Individual feature values are derived.
 */

export const featureDefinitions =
  pgTable(
    "feature_definitions",
    {
      featureId: text(
        "feature_id"
      ).primaryKey(),

      name: text(
        "name"
      ).notNull(),

      description:
        text(
          "description"
        ).notNull(),

      entityType:
        text(
          "entity_type"
        ).notNull(),

      valueType:
        text(
          "value_type"
        ).notNull(),

      version:
        text(
          "version"
        ).notNull(),

      calculation:
        text(
          "calculation"
        ).notNull(),

      requiredSignals:
        jsonb(
          "required_signals"
        )
          .notNull()
          .default([]),

      leakageRisk:
        text(
          "leakage_risk"
        )
          .notNull()
          .default("UNKNOWN"),

      productionEligible:
        boolean(
          "production_eligible"
        )
          .notNull()
          .default(false),

      createdAt:
        timestamp(
          "created_at",
          {
            withTimezone: true
          }
        )
          .notNull()
          .defaultNow()
    }
  );

/**
 * FEATURE VALUES
 */

export const featureValues =
  pgTable(
    "feature_values",
    {
      id: uuid("id")
        .defaultRandom()
        .primaryKey(),

      featureId: text(
        "feature_id"
      )
        .notNull()
        .references(
          () =>
            featureDefinitions
              .featureId
        ),

      entityId: text(
        "entity_id"
      ).notNull(),

      numericValue:
        doublePrecision(
          "numeric_value"
        ),

      textValue:
        text(
          "text_value"
        ),

      asOf: timestamp(
        "as_of",
        {
          withTimezone: true
        }
      ).notNull(),

      sourceWindowStart:
        timestamp(
          "source_window_start",
          {
            withTimezone: true
          }
        ),

      sourceWindowEnd:
        timestamp(
          "source_window_end",
          {
            withTimezone: true
          }
        ),

      createdAt:
        timestamp(
          "created_at",
          {
            withTimezone: true
          }
        )
          .notNull()
          .defaultNow()
    },
    (table) => ({
      featureEntityTimeUnique:
        uniqueIndex(
          "feature_values_entity_time_unique"
        ).on(
          table.featureId,
          table.entityId,
          table.asOf
        )
    })
  );

/**
 * DATASET DEFINITIONS
 */

export const datasetDefinitions =
  pgTable(
    "dataset_definitions",
    {
      datasetId: text(
        "dataset_id"
      ).primaryKey(),

      name: text(
        "name"
      ).notNull(),

      purpose: text(
        "purpose"
      ).notNull(),

      entityType:
        text(
          "entity_type"
        ).notNull(),

      targetDefinition:
        jsonb(
          "target_definition"
        ),

      featureIds:
        jsonb(
          "feature_ids"
        )
          .notNull()
          .default([]),

      splitStrategy:
        jsonb(
          "split_strategy"
        )
          .notNull(),

      version:
        text(
          "version"
        ).notNull(),

      createdAt:
        timestamp(
          "created_at",
          {
            withTimezone: true
          }
        )
          .notNull()
          .defaultNow()
    }
  );

/**
 * IMMUTABLE DATASET SNAPSHOTS
 */

export const datasetSnapshots =
  pgTable(
    "dataset_snapshots",
    {
      snapshotId: uuid(
        "snapshot_id"
      )
        .defaultRandom()
        .primaryKey(),

      datasetId: text(
        "dataset_id"
      )
        .notNull()
        .references(
          () =>
            datasetDefinitions
              .datasetId
        ),

      snapshotVersion:
        text(
          "snapshot_version"
        ).notNull(),

      sourceCutoffAt:
        timestamp(
          "source_cutoff_at",
          {
            withTimezone: true
          }
        ).notNull(),

      rowCount:
        integer(
          "row_count"
        ).notNull(),

      contentHash:
        text(
          "content_hash"
        ).notNull(),

      manifest:
        jsonb(
          "manifest"
        ).notNull(),

      status: text(
        "status"
      )
        .notNull()
        .default(
          "FROZEN"
        ),

      createdAt:
        timestamp(
          "created_at",
          {
            withTimezone: true
          }
        )
          .notNull()
          .defaultNow()
    },
    (table) => ({
      snapshotHashUnique:
        uniqueIndex(
          "dataset_snapshot_hash_unique"
        ).on(
          table.contentHash
        )
    })
  );