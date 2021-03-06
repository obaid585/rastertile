"""Test titiler.core.CacheControlMiddleware."""


from titiler.core.middleware import CacheControlMiddleware

from fastapi import FastAPI, Path

from starlette.testclient import TestClient


def test_cachecontrol_middleware_exclude():
    """Create App."""
    app = FastAPI()

    @app.get("/route1")
    async def route1():
        """route1."""
        return "yo"

    @app.get("/route2")
    async def route2():
        """route2."""
        return "yeah"

    @app.get("/route3")
    async def route3():
        """route3."""
        return "yeah"

    @app.get("/tiles/{z}/{x}/{y}")
    async def tiles(
        z: int = Path(..., ge=0, le=30, description="Mercator tiles's zoom level"),
        x: int = Path(..., description="Mercator tiles's column"),
        y: int = Path(..., description="Mercator tiles's row"),
    ):
        """tiles."""
        return "yeah"

    app.add_middleware(
        CacheControlMiddleware,
        cachecontrol="public",
        exclude_path={r"/route1", r"/route2", r"/tiles/[0-1]/.+"},
    )

    client = TestClient(app)

    response = client.get("/route1")
    assert not response.headers.get("Cache-Control")

    response = client.get("/route2")
    assert not response.headers.get("Cache-Control")

    response = client.get("/route3")
    assert response.headers["Cache-Control"] == "public"

    response = client.get("/tiles/0/1/1")
    assert not response.headers.get("Cache-Control")

    response = client.get("/tiles/3/1/1")
    assert response.headers["Cache-Control"] == "public"
