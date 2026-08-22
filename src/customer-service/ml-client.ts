import {
  env
} from "../config/env.js";

export type MlIntentPrediction = {
  label: string;
  score: number;
};

export type MlAnalysis = {
  sentiment: {
    model_id: string;
    model_version: string;
    label:
      | "POSITIVE"
      | "NEGATIVE";

    positive_probability:
      number;

    negative_probability:
      number;
  };

  intent: {
    model_id: string;
    model_version: string;

    predictions:
      MlIntentPrediction[];
  };
};

export class CustomerServiceMlError
  extends Error {

  constructor(
    message: string,
    public readonly causeData?:
      unknown
  ) {
    super(message);

    this.name =
      "CustomerServiceMlError";
  }
}

export async function
analyzeCustomerMessage(
  message: string
): Promise<MlAnalysis> {

  const controller =
    new AbortController();

  const timeout =
    setTimeout(
      () =>
        controller.abort(),
      env
        .CUSTOMER_SERVICE_ML_TIMEOUT_MS
    );

  try {
    const response =
      await fetch(
        `${
          env
            .CUSTOMER_SERVICE_ML_URL
        }/analyze`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body:
            JSON.stringify({
              text:
                message
            }),

          signal:
            controller.signal
        }
      );

    if (!response.ok) {
      throw new CustomerServiceMlError(
        `ML service returned ${
          response.status
        }`
      );
    }

    return (
      await response.json()
    ) as MlAnalysis;

  } catch (error) {
    if (
      error instanceof
      CustomerServiceMlError
    ) {
      throw error;
    }

    throw new CustomerServiceMlError(
      "Unable to analyze customer message",
      error
    );
  } finally {
    clearTimeout(
      timeout
    );
  }
}