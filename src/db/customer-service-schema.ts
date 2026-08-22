import {
  boolean,
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

export const serviceRiskEnum =
  pgEnum("service_risk", [
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL"
  ]);

export const serviceStatusEnum =
  pgEnum("service_status", [
    "OPEN",
    "AI_HANDLING",
    "ESCALATED",
    "WAITING_CUSTOMER",
    "WAITING_HUMAN",
    "RESOLVED",
    "CLOSED"
  ]);

export const resolutionAuthorityEnum =
  pgEnum(
    "resolution_authority",
    [
      "ANSWER_ONLY",
      "DRAFT_ACTION",
      "HUMAN_APPROVAL",
      "BOUNDED_AUTOMATION"
    ]
  );

export const serviceConversations =
  pgTable(
    "service_conversations",
    {
      id: uuid("id")
        .defaultRandom()
        .primaryKey(),

      conversationId:
        text(
          "conversation_id"
        )
          .notNull(),

      customerId:
        text(
          "customer_id"
        ),

      sessionId:
        text(
          "session_id"
        ),

      intent:
        text(
          "intent"
        )
          .notNull(),

      risk:
        serviceRiskEnum(
          "risk"
        )
          .notNull()
          .default("LOW"),

      status:
        serviceStatusEnum(
          "status"
        )
          .notNull()
          .default("OPEN"),

      resolutionAuthority:
        resolutionAuthorityEnum(
          "resolution_authority"
        )
          .notNull()
          .default("ANSWER_ONLY"),

      aiEligible:
        boolean(
          "ai_eligible"
        )
          .notNull()
          .default(true),

      humanRequested:
        boolean(
          "human_requested"
        )
          .notNull()
          .default(false),

      escalationReason:
        text(
          "escalation_reason"
        ),

      openedAt:
        timestamp(
          "opened_at",
          {
            withTimezone: true
          }
        )
          .notNull()
          .defaultNow(),

      resolvedAt:
        timestamp(
          "resolved_at",
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
          .defaultNow(),

      updatedAt:
        timestamp(
          "updated_at",
          {
            withTimezone: true
          }
        )
          .notNull()
          .defaultNow()
    },
    (table) => ({
      conversationUnique:
        uniqueIndex(
          "service_conversation_id_unique"
        ).on(
          table.conversationId
        ),

      customerIndex:
        index(
          "service_customer_idx"
        ).on(
          table.customerId
        ),

      statusIndex:
        index(
          "service_status_idx"
        ).on(
          table.status
        )
    })
  );

export const serviceMessages =
  pgTable(
    "service_messages",
    {
      id: uuid("id")
        .defaultRandom()
        .primaryKey(),

      messageId:
        text(
          "message_id"
        )
          .notNull(),

      conversationId:
        text(
          "conversation_id"
        )
          .notNull(),

      senderType:
        text(
          "sender_type"
        )
          .notNull(),

      content:
        text(
          "content"
        )
          .notNull(),

      sentiment:
        text(
          "sentiment"
        ),

      confidence:
        text(
          "confidence"
        ),

      evidenceRefs:
        jsonb(
          "evidence_refs"
        )
          .notNull()
          .default([]),

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
      messageUnique:
        uniqueIndex(
          "service_message_id_unique"
        ).on(
          table.messageId
        ),

      conversationIndex:
        index(
          "service_message_conversation_idx"
        ).on(
          table.conversationId
        )
    })
  );

export const serviceInterventions =
  pgTable(
    "service_interventions",
    {
      id: uuid("id")
        .defaultRandom()
        .primaryKey(),

      interventionId:
        text(
          "intervention_id"
        )
          .notNull(),

      customerId:
        text(
          "customer_id"
        ),

      sessionId:
        text(
          "session_id"
        ),

      interventionType:
        text(
          "intervention_type"
        )
          .notNull(),

      triggerType:
        text(
          "trigger_type"
        )
          .notNull(),

      reason:
        text(
          "reason"
        )
          .notNull(),

      status:
        text(
          "status"
        )
          .notNull()
          .default("CANDIDATE"),

      shown:
        boolean(
          "shown"
        )
          .notNull()
          .default(false),

      dismissed:
        boolean(
          "dismissed"
        )
          .notNull()
          .default(false),

      converted:
        boolean(
          "converted"
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
    },
    (table) => ({
      interventionUnique:
        uniqueIndex(
          "service_intervention_id_unique"
        ).on(
          table.interventionId
        ),

      sessionIndex:
        index(
          "service_intervention_session_idx"
        ).on(
          table.sessionId
        )
    })
  );

export const serviceResolutionEvents =
  pgTable(
    "service_resolution_events",
    {
      id: uuid("id")
        .defaultRandom()
        .primaryKey(),

      resolutionId:
        text(
          "resolution_id"
        )
          .notNull(),

      conversationId:
        text(
          "conversation_id"
        )
          .notNull(),

      resolutionType:
        text(
          "resolution_type"
        )
          .notNull(),

      authority:
        resolutionAuthorityEnum(
          "authority"
        )
          .notNull(),

      approvedBy:
        text(
          "approved_by"
        ),

      metadata:
        jsonb(
          "metadata"
        )
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
      resolutionUnique:
        uniqueIndex(
          "service_resolution_id_unique"
        ).on(
          table.resolutionId
        )
    })
  );