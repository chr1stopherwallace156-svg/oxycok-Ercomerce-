export type DatasetSplitStrategy =
  | {
      type:
        "TEMPORAL";

      trainEnd:
        string;

      validationEnd:
        string;

      testEnd:
        string;
    }
  | {
      type:
        "RANDOM";

      trainPercent:
        number;

      validationPercent:
        number;

      testPercent:
        number;

      seed:
        number;
    };

export type DatasetManifest = {
  datasetId: string;

  version: string;

  purpose: string;

  createdAt: string;

  sourceCutoffAt: string;

  entityType: string;

  featureIds: string[];

  target?: {
    name: string;

    horizon?: string;
  };

  splitStrategy:
    DatasetSplitStrategy;

  rowCount: number;

  contentHash: string;
};