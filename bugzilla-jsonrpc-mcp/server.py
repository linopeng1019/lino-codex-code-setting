#!/usr/bin/env python3
"""MCP stdio server that queries Bugzilla via JSON-RPC API."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SERVER_NAME = "Bugzilla JSON-RPC"
SERVER_VERSION = "0.1.0"
DEFAULT_PROTOCOL_VERSION = "2025-03-26"
DEFAULT_INCLUDE_FIELDS = (
    "id,product,component,assigned_to,status,resolution,"
    "summary,last_change_time"
)


class BugzillaError(Exception):
    """Raised when Bugzilla JSON-RPC returns an error."""


@dataclass
class BugzillaClient:
    """Simple Bugzilla JSON-RPC client."""

    base_url: str
    api_key: str
    timeout_sec: int = 20

    def call(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call a Bugzilla JSON-RPC method and return the decoded response."""
        payload = {
            "jsonrpc": "1.1",
            "method": method,
            "params": [params],
            "id": 1,
        }
        query = urlencode({"api_key": self.api_key}) if self.api_key else ""
        endpoint = f"{self.base_url}/jsonrpc.cgi"
        if query:
            endpoint = f"{endpoint}?{query}"
        req = Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(req, timeout=self.timeout_sec) as response:
            body = response.read().decode("utf-8")
        result = json.loads(body)
        error = result.get("error")
        if error:
            raise BugzillaError(json.dumps(error, ensure_ascii=True))
        return result


class McpServer:
    """Minimal MCP server for stdio transport."""

    def __init__(self, client: BugzillaClient) -> None:
        self.client = client

    def send(self, payload: Dict[str, Any]) -> None:
        """Write one MCP-framed JSON message to stdout."""
        data = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        header = f"Content-Length: {len(data)}\r\n\r\n".encode("ascii")
        sys.stdout.buffer.write(header + data)
        sys.stdout.buffer.flush()

    def read_message(self) -> Optional[Dict[str, Any]]:
        """Read one MCP-framed JSON message from stdin."""
        content_length: Optional[int] = None
        while True:
            line = sys.stdin.buffer.readline()
            if not line:
                return None
            if line in (b"\r\n", b"\n"):
                break
            header_line = line.decode("ascii", errors="ignore").strip()
            if not header_line:
                continue
            key, _, value = header_line.partition(":")
            if key.lower() == "content-length":
                content_length = int(value.strip())
        if content_length is None:
            return None
        body = sys.stdin.buffer.read(content_length)
        if not body:
            return None
        return json.loads(body.decode("utf-8"))

    @staticmethod
    def _text_result(
        text: str,
        structured: Optional[Dict[str, Any]] = None,
        is_error: bool = False,
    ) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "content": [{"type": "text", "text": text}],
            "isError": is_error,
        }
        if structured is not None:
            result["structuredContent"] = structured
        return result

    @staticmethod
    def _to_int(value: Any, field: str) -> int:
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"`{field}` must be an integer") from exc

    def handle_tools_call(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch tools/call requests."""
        if name == "server_url":
            return self._text_result(self.client.base_url, {"result": self.client.base_url})

        if name == "bug_url":
            bug_id = self._to_int(arguments.get("bug_id"), "bug_id")
            url = f"{self.client.base_url}/show_bug.cgi?id={bug_id}"
            return self._text_result(url, {"result": url})

        if name == "bug_info":
            bug_id = self._to_int(arguments.get("id"), "id")
            rpc = self.client.call("Bug.get", {"ids": [bug_id]})
            bugs = rpc.get("result", {}).get("bugs", [])
            if not bugs:
                raise BugzillaError(f"Bug {bug_id} not found")
            bug = bugs[0]
            return self._text_result(
                json.dumps(bug, ensure_ascii=False),
                bug,
            )

        if name == "bug_comments":
            bug_id = self._to_int(arguments.get("id"), "id")
            include_private = bool(arguments.get("include_private_comments", False))
            rpc = self.client.call("Bug.comments", {"ids": [bug_id]})
            comments = (
                rpc.get("result", {})
                .get("bugs", {})
                .get(str(bug_id), {})
                .get("comments", [])
            )
            if not include_private:
                comments = [item for item in comments if not item.get("is_private", False)]
            wrapped = {"result": comments}
            return self._text_result(
                json.dumps(wrapped, ensure_ascii=False),
                wrapped,
            )

        if name == "bugs_quicksearch":
            query = str(arguments.get("query", "")).strip()
            if not query:
                raise ValueError("`query` is required")
            status = arguments.get("status", "ALL")
            limit = self._to_int(arguments.get("limit", 50), "limit")
            offset = self._to_int(arguments.get("offset", 0), "offset")
            include_fields = arguments.get("include_fields", DEFAULT_INCLUDE_FIELDS)
            if include_fields is None:
                include_fields = DEFAULT_INCLUDE_FIELDS
            if isinstance(include_fields, str):
                parsed_fields = [item.strip() for item in include_fields.split(",") if item.strip()]
            elif isinstance(include_fields, list):
                parsed_fields = [str(item) for item in include_fields]
            else:
                raise ValueError("`include_fields` must be string, list, or null")
            search_payload: Dict[str, Any] = {
                "quicksearch": query,
                "limit": limit,
                "offset": offset,
            }
            if parsed_fields:
                search_payload["include_fields"] = parsed_fields
            if status and str(status).upper() != "ALL":
                search_payload["status"] = status
            rpc = self.client.call("Bug.search", search_payload)
            bugs = rpc.get("result", {}).get("bugs", [])
            wrapped = {"result": bugs}
            return self._text_result(
                json.dumps(wrapped, ensure_ascii=False),
                wrapped,
            )

        raise ValueError(f"Unknown tool: {name}")

    def handle_request(self, msg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle one incoming JSON-RPC request or notification."""
        method = msg.get("method")
        request_id = msg.get("id")

        if method == "notifications/initialized":
            return None

        if method == "ping":
            return {"jsonrpc": "2.0", "id": request_id, "result": {}}

        if method == "initialize":
            params = msg.get("params", {})
            protocol = params.get("protocolVersion", DEFAULT_PROTOCOL_VERSION)
            result = {
                "protocolVersion": protocol,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            }
            return {"jsonrpc": "2.0", "id": request_id, "result": result}

        if method == "tools/list":
            tools = [
                {
                    "name": "bug_info",
                    "description": "Returns full information for a bug id.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                        "required": ["id"],
                    },
                },
                {
                    "name": "bug_comments",
                    "description": "Returns comments for a bug id.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "include_private_comments": {"type": "boolean", "default": False},
                        },
                        "required": ["id"],
                    },
                },
                {
                    "name": "bugs_quicksearch",
                    "description": "Search bugs using quicksearch syntax.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "status": {"type": ["string", "null"], "default": "ALL"},
                            "include_fields": {
                                "type": ["string", "array", "null"],
                                "default": DEFAULT_INCLUDE_FIELDS,
                            },
                            "limit": {"type": ["integer", "null"], "default": 50},
                            "offset": {"type": ["integer", "null"], "default": 0},
                        },
                        "required": ["query"],
                    },
                },
                {
                    "name": "server_url",
                    "description": "Returns Bugzilla base URL.",
                    "inputSchema": {"type": "object", "properties": {}},
                },
                {
                    "name": "bug_url",
                    "description": "Returns the show_bug.cgi URL for a bug id.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"bug_id": {"type": "integer"}},
                        "required": ["bug_id"],
                    },
                },
            ]
            return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": tools}}

        if method == "tools/call":
            params = msg.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments") or {}
            if not isinstance(arguments, dict):
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": self._text_result(
                        "`arguments` must be an object",
                        is_error=True,
                    ),
                }
            try:
                tool_result = self.handle_tools_call(str(tool_name), arguments)
                return {"jsonrpc": "2.0", "id": request_id, "result": tool_result}
            except (BugzillaError, ValueError) as exc:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": self._text_result(str(exc), is_error=True),
                }
            except Exception as exc:  # pragma: no cover
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": self._text_result(
                        f"Unexpected error: {exc}",
                        is_error=True,
                    ),
                }

        if request_id is None:
            return None
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }

    def run(self) -> None:
        """Main server loop."""
        while True:
            msg = self.read_message()
            if msg is None:
                return
            response = self.handle_request(msg)
            if response is not None:
                self.send(response)


def _get_env(name: str, default: str = "") -> str:
    value = os.environ.get(name, default).strip()
    return value


def main() -> int:
    """Entrypoint."""
    base_url = _get_env("BUGZILLA_BASE_URL", "http://e-andes.andestech.com/bugzilla5")
    api_key = _get_env("BUGZILLA_API_KEY")
    if not api_key:
        print("BUGZILLA_API_KEY is required", file=sys.stderr)
        return 2
    client = BugzillaClient(base_url=base_url.rstrip("/"), api_key=api_key)
    server = McpServer(client=client)
    server.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
