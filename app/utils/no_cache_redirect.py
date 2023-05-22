import time

from fastapi.responses import RedirectResponse


def redirect_no_cache(url: str):
    response = RedirectResponse(url=url, status_code=303)
    response.headers.append(
        key="Cache-Control",
        value="no-cache"
    )
    response.headers.append(
        key="Pragma",
        value="no-cache"
    )
    return response
