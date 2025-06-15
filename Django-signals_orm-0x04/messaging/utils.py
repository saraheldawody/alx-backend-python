# Django-Chat/Models.py (or utils.py)

def get_threaded_messages(parent):
    """
    Recursively fetch all nested replies of a message.
    """
    thread = []
    for reply in parent.replies.all().order_by('sent_at'):
        thread.append({
            'message_id': str(reply.message_id),
            'content': reply.content,
            'sender': reply.sender.username,
            'sent_at': reply.sent_at,
            'edited': reply.edited,
            'replies': get_threaded_messages(reply)
        })
    return thread
