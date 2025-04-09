from fastapi import HTTPException, status


def http_exception():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


def http_forbiden():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied")


def http_badrequest():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Bad Request")
