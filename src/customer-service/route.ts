import crypto from "node:crypto";

import {
  Router
} from "express";

import {
  z
} from "zod";

import {
  evaluateServiceRequest
} from "./escalation.js";

import {
  persistConversation,
  persistCustomerMessage
} from "./repository.js";

export const customerServiceRouter =
  Router();

const RequestSchema =
  z.object({
    conversationId:
      z.string().min(1),

    customerId:
      z.string().optional(),

    sessionId:
      z.string().optional(),

    message:
      z.string()
        .min(1)
        .max(5000),

    humanRequested:
      z.boolean()
        .optional()
  });

customerServiceRouter.post(
  "/message",
  async (
    req,
    res
  ) => {
    const parsed =
      RequestSchema.safeParse(
        req.body
      );

    if (
      !parsed.success
    ) {
      res
        .status(400)
        .json({
          status:
            "invalid_request",

          errors:
            parsed
              .error
              .issues
        });

      return;
    }

    const request =
      parsed.data;

    const decision =
      evaluateServiceRequest(
        request
      );

    const messageId =
      crypto
        .randomUUID();

    try {
      await persistConversation(
        request,
        decision
      );

      await persistCustomerMessage({
        messageId,

        conversationId:
          request
            .conversationId,

        content:
          request.message
      });

      res.json({
        status:
          "accepted",

        conversationId:
          request
            .conversationId,

        decision
      });
    } catch (error) {
      console.error(
        error
      );

      res
        .status(500)
        .json({
          status:
            "persistence_failed"
        });
    }
  }
);