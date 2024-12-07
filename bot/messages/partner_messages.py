def invalid_format():
    return "Invalid username format. Usernames must start with '@'."


def unexpected_err_msg(username: str, error: Exception) -> str:
    return (
        f"Unexpected error resolving partner ID for {username!r}: {error!r}. "
        f"Please try again later."
    )


def invitation_link_created(username):
    return (
        f"First time secure contact with {username!r} is requested.\n"
        f"Send link above to {username!r} to initiate secure channel."
    )
