def log_progress(sequence, every=None, size=None, with_time=True, name=''):
    from ipywidgets import IntProgress, HTML, HBox
    from IPython.display import display
    from datetime import datetime

    def format_time(time_value):
        return str(time_value).split(".")[0]

    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = int(size / 200)  # every 0.5%
    else:
        assert every is not None, 'sequence is iterator, set every'

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
        with_time = False
    else:
        progress = IntProgress(min=0, max=size, value=0)

    label = HTML()
    box = HBox(children=[label, progress])
    display(box)

    time_started = datetime.now()
    index = 0
    try:
        for index, record in enumerate(sequence, 0):
            if index % every == 0:
                if is_iterator:
                    label.value = '{name} {index} / ?'.format(
                        name=name,
                        index=index
                    )
                else:
                    if with_time:
                        if index > 0:
                            time_elapsed = datetime.now() - time_started
                            time_left = size / index * time_elapsed - time_elapsed
                            time_status = "| ETA: {}".format(format_time(time_left))
                        else:
                            time_status = "???"
                    else:
                        time_status = ""

                    progress.value = index
                    label.value = u'{name}: {index} / {size} {time}'.format(
                        name=name,
                        index=index,
                        size=size,
                        time=time_status
                    )

            yield record
    except:
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        index += 1
        progress.value = index
        label.value = "{name} {index} / {size} | Time elapsed {time_elapsed}".format(
            name=name,
            index=str(index or '?'),
            size=size,
            time_elapsed=format_time(datetime.now() - time_started),
        )
