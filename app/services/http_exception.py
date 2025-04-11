from fastapi import HTTPException, status


def http_notfound(detail=None):
    if detail:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


def http_forbidden(detail=None):
    if detail:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    else:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied1")


def http_badrequest(detail=None):
    if detail:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    else:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request")
