from time import time
from fastapi import Request


class ProcessTime:
    def __init__(self):
        pass

    async def __call__(self, request: Request, call_next):
        start_time = time()
        response = await call_next(request)
        process_time = time() - start_time
        response.headers["x-process-time"] = str(process_time)
        return response
