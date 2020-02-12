""" Error handler """


def get_error_details(details, error_type):
    """
    Get the Error Response
    :param details: String
    :param error_type: String
    :return: Dict
    """
    return dict(error=details,
                error_type=error_type)
