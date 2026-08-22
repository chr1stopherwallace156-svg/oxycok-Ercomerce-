export type ServiceIntent =
  | "PRODUCT_QUESTION"
  | "ORDER_STATUS"
  | "SHIPPING"
  | "RETURN"
  | "REFUND"
  | "CANCELLATION"
  | "PRODUCT_FIT"
  | "PRODUCT_COMPARISON"
  | "PAYMENT"
  | "COMPLAINT"
  | "OTHER";

export type ServiceRisk =
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | "CRITICAL";

export type ResolutionAuthority =
  | "ANSWER_ONLY"
  | "DRAFT_ACTION"
  | "HUMAN_APPROVAL"
  | "BOUNDED_AUTOMATION";

export type ServiceStatus =
  | "OPEN"
  | "AI_HANDLING"
  | "ESCALATED"
  | "WAITING_CUSTOMER"
  | "WAITING_HUMAN"
  | "RESOLVED"
  | "CLOSED";

export type ServiceRequest = {
  conversationId: string;

  customerId?: string;

  sessionId?: string;

  message: string;

  intent?: ServiceIntent;

  risk?: ServiceRisk;

  humanRequested?: boolean;

  metadata?: Record<
    string,
    unknown
  >;
};

export type ServiceDecision = {
  conversationId: string;

  intent:
    ServiceIntent;

  risk:
    ServiceRisk;

  authority:
    ResolutionAuthority;

  shouldEscalate:
    boolean;

  escalationReason?: string;

  canAnswerWithAI:
    boolean;
};

export type InterventionCandidate = {
  interventionId: string;

  customerId?: string;

  sessionId?: string;

  triggerType: string;

  interventionType:
    | "CHAT_INVITE"
    | "PRODUCT_HELP"
    | "ORDER_HELP"
    | "HUMAN_ESCALATION";

  reason: string;

  priority:
    "LOW"
    | "MEDIUM"
    | "HIGH";
};