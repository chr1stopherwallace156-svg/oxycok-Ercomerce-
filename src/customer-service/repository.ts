import {
  db
} from "../db/client.js";

import {
  serviceConversations,
  serviceInterventions,
  serviceMessages
} from "../db/customer-service-schema.js";

import type {
  InterventionCandidate,
  ServiceDecision,
  ServiceRequest
} from "./types.js";

export async function persistConversation(
  request: ServiceRequest,
  decision: ServiceDecision
) {
  await db
    .insert(
      serviceConversations
    )
    .values({
      conversationId:
        request.conversationId,

      customerId:
        request.customerId,

      sessionId:
        request.sessionId,

      intent:
        decision.intent,

      risk:
        decision.risk,

      status:
        decision.shouldEscalate
          ? "ESCALATED"
          : "AI_HANDLING",

      resolutionAuthority:
        decision.authority,

      aiEligible:
        decision.canAnswerWithAI,

      humanRequested:
        request.humanRequested ??
        false,

      escalationReason:
        decision
          .escalationReason
    })
    .onConflictDoNothing();
}

export async function persistCustomerMessage(
  input: {
    messageId: string;

    conversationId: string;

    content: string;

    evidenceRefs?: string[];
  }
) {
  await db
    .insert(
      serviceMessages
    )
    .values({
      messageId:
        input.messageId,

      conversationId:
        input.conversationId,

      senderType:
        "CUSTOMER",

      content:
        input.content,

      evidenceRefs:
        input.evidenceRefs ??
        []
    })
    .onConflictDoNothing();
}

export async function persistIntervention(
  candidate:
    InterventionCandidate
) {
  await db
    .insert(
      serviceInterventions
    )
    .values({
      interventionId:
        candidate
          .interventionId,

      customerId:
        candidate
          .customerId,

      sessionId:
        candidate
          .sessionId,

      interventionType:
        candidate
          .interventionType,

      triggerType:
        candidate
          .triggerType,

      reason:
        candidate.reason,

      status:
        "CANDIDATE"
    })
    .onConflictDoNothing();
}