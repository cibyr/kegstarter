from ..shared import get_user_balance


def get_user_votes(request):
    # Must be logged in to have a balance
    if request.user.id:
        votes = get_user_balance(request.user)
    else:
        votes = None

    return {'get_user_votes': votes,}