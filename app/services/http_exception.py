from fastapi import HTTPException, status


def http_notfound():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


def http_forbidden():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied1")


def http_badrequest():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Bad Request")
