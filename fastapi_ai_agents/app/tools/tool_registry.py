from app.tools import web_search_tool, rag_tool, n8n_tool

class ToolRegistry:
    def __init__(self):
        self.tools = {
            # "rag_tool": rag_tool.run,
            "search_tool": web_search_tool.search_web,
            "n8n_tool": n8n_tool.send_to_n8n
        }

    def get_tool(self, name):
        return self.tools[name]

    def get_openai_schema(self):
        # Return all tools in OpenAI format
        return [t.schema for t in [ web_search_tool, n8n_tool]]
        # return [t.schema for t in [rag_tool, web_search_tool, n8n_tool]]


tool_registry = ToolRegistry()
