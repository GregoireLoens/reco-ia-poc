#!/usr/bin/env python3
"""
Simple MCP Server with Hello World functionality
"""
import asyncio
import json
from typing import Any, Dict
from datetime import datetime
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Create FastAPI app for MCP server
app = FastAPI(title="MCP Hello World Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for requests
class ToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any] = {}

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: int
    method: str
    params: Dict[str, Any] = {}

# Tool functions
def hello_world(name: str = "World") -> str:
    """Say hello to someone"""
    return f"Hello, {name}!"

def get_current_time() -> str:
    """Get the current time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.get("/")
async def root():
    return {"message": "MCP Hello World Server is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/mcp")
async def handle_mcp_request(request: MCPRequest):
    """Handle MCP requests"""
    try:
        if request.method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request.id,
                "result": {
                    "tools": [
                        {
                            "name": "hello_world",
                            "description": "Say hello to someone",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Name to greet"
                                    }
                                }
                            }
                        },
                        {
                            "name": "get_current_time",
                            "description": "Get the current time",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        }
                    ]
                }
            }
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            arguments = request.params.get("arguments", {})

            if tool_name == "hello_world":
                name = arguments.get("name", "World")
                result = hello_world(name)
                return {
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "result": {
                        "content": [{"type": "text", "text": result}]
                    }
                }
            elif tool_name == "get_current_time":
                result = get_current_time()
                return {
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "result": {
                        "content": [{"type": "text", "text": result}]
                    }
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool '{tool_name}' not found"
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{request.method}' not supported"
                }
            }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }

@app.get("/tools")
async def list_tools():
    """List available tools"""
    return {
        "tools": [
            {
                "name": "hello_world",
                "description": "Say hello to someone",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name to greet"}
                    }
                }
            },
            {
                "name": "get_current_time",
                "description": "Get the current time"
            }
        ]
    }

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, request: Dict[str, Any]):
    """Call a specific tool"""
    try:
        if tool_name == "hello_world":
            name = request.get("arguments", {}).get("name", "World")
            result = hello_world(name)
        elif tool_name == "get_current_time":
            result = get_current_time()
        else:
            return {"error": f"Tool '{tool_name}' not found"}

        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("🚀 Starting MCP Hello World Server...")
    uvicorn.run(app, host="0.0.0.0", port=8001)