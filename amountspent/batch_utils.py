
def generate_batches(iterable, batch_size_limit):
    """
    Generator that yields lists of length size batch_size_limit containing
    objects yielded by the iterable.
    """
    batch = []

    for item in iterable:
        if len(batch) == batch_size_limit:
            yield batch
            batch = []
        batch.append(item)

    if len(batch):
        yield batch