#!/usr/bin/env python3
"""
MCP Server with Sylius Product Integration
"""
import asyncio
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Import des modèles Sylius
from models import get_db, Product, ProductVariant, ProductTranslation

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

def get_sylius_products(limit: int = 10, offset: int = 0, db: Session = None) -> List[Dict[str, Any]]:
    """Get products from Sylius database"""
    if db is None:
        return []

    try:
        products = db.query(Product).filter(Product.enabled == True).offset(offset).limit(limit).all()

        result = []
        for product in products:
            product_data = {
                "id": product.id,
                "code": product.code,
                "name": product.get_name(),
                "description": product.get_description(),
                "enabled": product.enabled,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "variants": []
            }

            # Ajouter les variants
            for variant in product.variants:
                if variant.enabled:
                    variant_data = {
                        "id": variant.id,
                        "code": variant.code,
                        "price": variant.get_price(),
                        "on_hand": variant.on_hand,
                        "tracked": variant.tracked
                    }
                    product_data["variants"].append(variant_data)

            result.append(product_data)

        return result
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []

def get_sylius_product_by_code(code: str, db: Session = None) -> Optional[Dict[str, Any]]:
    """Get a specific product by code from Sylius database"""
    if db is None:
        return None

    try:
        product = db.query(Product).filter(Product.code == code, Product.enabled == True).first()

        if not product:
            return None

        product_data = {
            "id": product.id,
            "code": product.code,
            "name": product.get_name(),
            "description": product.get_description(),
            "enabled": product.enabled,
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "variants": []
        }

        # Ajouter les variants
        for variant in product.variants:
            if variant.enabled:
                variant_data = {
                    "id": variant.id,
                    "code": variant.code,
                    "price": variant.get_price(),
                    "on_hand": variant.on_hand,
                    "tracked": variant.tracked
                }
                product_data["variants"].append(variant_data)

        return product_data
    except Exception as e:
        print(f"Error fetching product {code}: {e}")
        return None

def search_sylius_products(query: str, limit: int = 10, db: Session = None) -> List[Dict[str, Any]]:
    """Search products by name or description"""
    if db is None:
        return []

    try:
        # Recherche dans les traductions
        products = db.query(Product).join(Product.translations).filter(
            Product.enabled == True,
            (ProductTranslation.name.contains(query) | ProductTranslation.description.contains(query))
        ).limit(limit).all()

        result = []
        for product in products:
            product_data = {
                "id": product.id,
                "code": product.code,
                "name": product.get_name(),
                "description": product.get_description(),
                "enabled": product.enabled,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "variants": []
            }

            # Ajouter les variants
            for variant in product.variants:
                if variant.enabled:
                    variant_data = {
                        "id": variant.id,
                        "code": variant.code,
                        "price": variant.get_price(),
                        "on_hand": variant.on_hand,
                        "tracked": variant.tracked
                    }
                    product_data["variants"].append(variant_data)

            result.append(product_data)

        return result
    except Exception as e:
        print(f"Error searching products: {e}")
        return []

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
                        },
                        {
                            "name": "get_sylius_products",
                            "description": "Get products from Sylius e-commerce platform",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "limit": {
                                        "type": "integer",
                                        "description": "Maximum number of products to return",
                                        "default": 10
                                    },
                                    "offset": {
                                        "type": "integer",
                                        "description": "Number of products to skip",
                                        "default": 0
                                    }
                                }
                            }
                        },
                        {
                            "name": "get_sylius_product_by_code",
                            "description": "Get a specific product by its code from Sylius",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "code": {
                                        "type": "string",
                                        "description": "Product code to search for"
                                    }
                                },
                                "required": ["code"]
                            }
                        },
                        {
                            "name": "search_sylius_products",
                            "description": "Search products by name or description in Sylius",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "Search query"
                                    },
                                    "limit": {
                                        "type": "integer",
                                        "description": "Maximum number of products to return",
                                        "default": 10
                                    }
                                },
                                "required": ["query"]
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
            elif tool_name == "get_sylius_products":
                # Obtenir une session DB
                db = next(get_db())
                limit = arguments.get("limit", 10)
                offset = arguments.get("offset", 0)
                products = get_sylius_products(limit=limit, offset=offset, db=db)
                result = json.dumps(products, indent=2, ensure_ascii=False)
                return {
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "result": {
                        "content": [{"type": "text", "text": result}]
                    }
                }
            elif tool_name == "get_sylius_product_by_code":
                code = arguments.get("code")
                if not code:
                    return {
                        "jsonrpc": "2.0",
                        "id": request.id,
                        "error": {
                            "code": -32602,
                            "message": "Parameter 'code' is required"
                        }
                    }
                db = next(get_db())
                product = get_sylius_product_by_code(code=code, db=db)
                if product is None:
                    result = f"Product with code '{code}' not found"
                else:
                    result = json.dumps(product, indent=2, ensure_ascii=False)
                return {
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "result": {
                        "content": [{"type": "text", "text": result}]
                    }
                }
            elif tool_name == "search_sylius_products":
                query = arguments.get("query")
                if not query:
                    return {
                        "jsonrpc": "2.0",
                        "id": request.id,
                        "error": {
                            "code": -32602,
                            "message": "Parameter 'query' is required"
                        }
                    }
                db = next(get_db())
                limit = arguments.get("limit", 10)
                products = search_sylius_products(query=query, limit=limit, db=db)
                result = json.dumps(products, indent=2, ensure_ascii=False)
                return {
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "result": {
                        "content": [{"type": "text", "text": f"Found {len(products)} products matching '{query}':\n{result}"}]
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
            },
            {
                "name": "get_sylius_products",
                "description": "Get products from Sylius e-commerce platform",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Maximum number of products to return", "default": 10},
                        "offset": {"type": "integer", "description": "Number of products to skip", "default": 0}
                    }
                }
            },
            {
                "name": "get_sylius_product_by_code",
                "description": "Get a specific product by its code from Sylius",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Product code to search for"}
                    },
                    "required": ["code"]
                }
            },
            {
                "name": "search_sylius_products",
                "description": "Search products by name or description in Sylius",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "limit": {"type": "integer", "description": "Maximum number of products to return", "default": 10}
                    },
                    "required": ["query"]
                }
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
        elif tool_name == "get_sylius_products":
            db = next(get_db())
            limit = request.get("arguments", {}).get("limit", 10)
            offset = request.get("arguments", {}).get("offset", 0)
            products = get_sylius_products(limit=limit, offset=offset, db=db)
            result = products
        elif tool_name == "get_sylius_product_by_code":
            code = request.get("arguments", {}).get("code")
            if not code:
                return {"error": "Parameter 'code' is required"}
            db = next(get_db())
            product = get_sylius_product_by_code(code=code, db=db)
            result = product if product else f"Product with code '{code}' not found"
        elif tool_name == "search_sylius_products":
            query = request.get("arguments", {}).get("query")
            if not query:
                return {"error": "Parameter 'query' is required"}
            db = next(get_db())
            limit = request.get("arguments", {}).get("limit", 10)
            products = search_sylius_products(query=query, limit=limit, db=db)
            result = products
        else:
            return {"error": f"Tool '{tool_name}' not found"}

        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("🚀 Starting MCP Hello World Server...")
    uvicorn.run(app, host="0.0.0.0", port=8001)