"""Tool and capability schema."""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ToolDef:
    name: str
    description: str = ""
    requires: list[str] = field(default_factory=list)
    produces: list[str] = field(default_factory=list)
    cost: float = 0.0
    latency: float = 0.0
    reliability: float = 0.99
    provider: str = ""
    credentials: list[str] = field(default_factory=list)

@dataclass
class Capability:
    name: str
    description: str = ""

@dataclass
class Route:
    route_id: int
    steps: list[str]
    cost: float
    latency: float
    reliability: float

# Pre-built tool definitions
DEFAULT_TOOLS = [
    ToolDef("github.read_issue", "Read a GitHub issue", ["repo", "issue_number"], ["issue_text"], 0, 0.3, 0.99),
    ToolDef("github.search_code", "Search code in repo", ["repo", "query"], ["source_context"], 0, 0.5, 0.98),
    ToolDef("github.create_pr", "Create a pull request", ["repo", "patch", "title"], ["pull_request"], 0, 0.4, 0.99),
    ToolDef("model.patch", "Generate code patch", ["source_context", "issue_text"], ["patch"], 0.03, 3.0, 0.92, "deepseek"),
    ToolDef("gpt.patch", "Generate code patch (GPT)", ["source_context", "issue_text"], ["patch"], 0.04, 2.0, 0.94, "openai"),
    ToolDef("pytest.run", "Run tests on patch", ["patch", "repo"], ["tested_patch"], 0, 2.0, 0.98),
    ToolDef("filesystem.read", "Read local file", ["path"], ["file_content"], 0, 0.01, 1.0),
    ToolDef("filesystem.write", "Write local file", ["path", "content"], ["file_written"], 0, 0.01, 1.0),
    ToolDef("llm.summarize", "Summarize text", ["text"], ["summary"], 0.01, 1.0, 0.95, "deepseek"),
    ToolDef("llm.classify", "Classify text", ["text", "classes"], ["classification"], 0.005, 0.5, 0.90, "deepseek"),
    ToolDef("web.search", "Search the web", ["query"], ["search_results"], 0, 1.0, 0.85),
    ToolDef("web.fetch", "Fetch a URL", ["url"], ["page_content"], 0, 0.5, 0.90),
    ToolDef("database.query", "Query a database", ["sql", "database"], ["query_results"], 0, 0.2, 0.99),
    ToolDef("email.send", "Send an email", ["to", "subject", "body"], ["email_sent"], 0, 1.0, 0.95),
    ToolDef("slack.post", "Post to Slack", ["channel", "message"], ["message_posted"], 0, 0.3, 0.98),
    ToolDef("calendar.create", "Create calendar event", ["title", "time", "attendees"], ["event_created"], 0, 0.2, 0.99),
    ToolDef("ssh.execute", "Execute remote command", ["host", "command", "credential"], ["command_output"], 0, 1.0, 0.95),
    ToolDef("docker.run", "Run Docker container", ["image", "command"], ["container_output"], 0, 2.0, 0.90),
    ToolDef("api.call", "Call REST API", ["url", "method", "body"], ["api_response"], 0, 0.5, 0.95),
    ToolDef("file.convert", "Convert file format", ["input_path", "output_format"], ["output_path"], 0, 0.3, 0.98),
]
