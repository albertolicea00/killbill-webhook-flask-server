def handle_payment_failed(event: object):
    """ """
    data = event.get_json()
    print(">>> Handling payment failed notification...")
    # print("with data : ", data)  # use to debug (comment when done)
