from .event import subscribe


def handle_page_loading_error_event(err: str):
    print("handle_user_registered_event", err)


def setup_log_handler():
    subscribe("page_loading_error", handle_page_loading_error_event)
