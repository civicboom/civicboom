
def init_worker_functions(w, extra_worker_functions=[]):
    """
    Pass worker object
    """
    from civicboom.worker.functions.send_notification     import send_notification
    from civicboom.worker.functions.process_media         import process_media
    from civicboom.worker.functions.profanity_check       import profanity_check
    from civicboom.worker.functions.content_notifications import content_notifications

    w.add_worker_function( send_notification     )
    w.add_worker_function( process_media         )
    w.add_worker_function( profanity_check       )
    w.add_worker_function( content_notifications )

    for f in extra_worker_functions:
        w.add_worker_function(f)