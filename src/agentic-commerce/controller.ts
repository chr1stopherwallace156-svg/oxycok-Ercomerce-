import {
  z
} from "zod";

export const AgentPlanSchema =
  z.object({
    objective:
      z.string(),

    nextAction:
      z.object({
        tool:
          z.string(),

        parameters:
          z.record(
            z.unknown()
          ),

        reason:
          z.string()
      }),

    requiresMoreInformation:
      z.boolean(),

    customerQuestion:
      z.string()
        .optional()
  });