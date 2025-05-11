from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

@router.get("/widget/openai-widget.html")
async def get_widget():
    """Serve the chat widget HTML file."""
    widget_path = Path(__file__).parent / "static" / "openai-widget.html"
    return FileResponse(widget_path) 