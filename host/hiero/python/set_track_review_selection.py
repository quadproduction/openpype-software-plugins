from openpype.hosts.hiero.api import get_timeline_selection


def run():
    track_items = get_timeline_selection()

    if not track_items:
        return

    for track_item in track_items:
        track_name = track_item.parentTrack().name()
        tags = track_item.tags()
        for tag in tags:
            metadata = tag.metadata()
            if metadata.hasKey("reviewTrack"):
                tag.metadata().setValue("tag.reviewTrack", track_name)
