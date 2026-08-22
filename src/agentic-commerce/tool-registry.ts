import type {
  AgentToolDefinition
} from "./types.js";

export class ToolRegistry {
  private readonly tools =
    new Map<
      string,
      AgentToolDefinition
    >();

  register(
    tool: AgentToolDefinition
  ): void {

    if (
      this.tools.has(
        tool.name
      )
    ) {
      throw new Error(
        `Duplicate tool registration: ${tool.name}`
      );
    }

    this.tools.set(
      tool.name,
      tool
    );
  }

  get(
    name: string
  ): AgentToolDefinition {

    const tool =
      this.tools.get(
        name
      );

    if (!tool) {
      throw new Error(
        `Unknown tool: ${name}`
      );
    }

    return tool;
  }

  list() {
    return Array.from(
      this.tools.values()
    ).map(
      tool => ({
        toolId:
          tool.toolId,

        name:
          tool.name,

        description:
          tool.description,

        risk:
          tool.risk,

        authority:
          tool.authority,

        readOnly:
          tool.readOnly
      })
    );
  }
}

export const toolRegistry =
  new ToolRegistry();