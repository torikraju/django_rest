from collections import namedtuple


def jwt_create_response_payload(token, user=None, request=None, issued_at=None):
    """
    Return data ready to be passed to serializer.

    Override this function if you need to include any additional data for
    serializer.

    Note that we are using `pk` field here - this is for forward compatibility
    with drf add-ons that might require `pk` field in order (eg. jsonapi).
    """

    response_payload = namedtuple('ResponsePayload', 'pk')
    # response_payload.pk = issued_at
    response_payload.token = {
        "token": token
    }
    # response_payload.user = user
    # response_payload.bunny = 'dsfsdf'

    return response_payload
