#!/usr/bin/env python3
"""
Simple test to verify Scalar FastAPI integration
"""

try:
    # Test importing scalar_fastapi
    from scalar_fastapi import get_scalar_api_reference, SearchHotKey
    print("✅ scalar-fastapi imported successfully")
    
    # Test that we can create a Scalar reference
    scalar_html = get_scalar_api_reference(
        openapi_url="http://localhost:8000/openapi.json",
        title="Test API",
        dark_mode=True,
        hide_search=False,
        search_hot_key=SearchHotKey.K,
        persist_auth=True,
        scalar_proxy_url="https://proxy.scalar.com",
    )
    
    print("✅ Scalar API reference generated successfully")
    print("✅ scalar-fastapi is properly configured and working!")
    
    # Verify it's an HTML response
    if scalar_html and "<html" in scalar_html.body.decode():
        print("✅ Scalar HTML documentation generated correctly")
    else:
        print("❌ Scalar HTML generation failed")
        
except ImportError as e:
    print(f"❌ Failed to import scalar-fastapi: {e}")
except Exception as e:
    print(f"❌ Error testing scalar-fastapi: {e}")
