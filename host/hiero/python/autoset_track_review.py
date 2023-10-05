import hiero.core


def get_track_items():
    # Get the active project
    project = hiero.core.projects()[-1]  # Assuming the last project is the active one

    # Get track items
    track_items = []
    for track in project.videoTracks():
        for item in track.items():
            track_items.append(item)

    return track_items


# Example usage
track_items = get_track_items()
for track_item in track_items:
    track_name = track_item.parentTrack().name()
    tags = track_item.tags()
    for tag in tags:
        metadata = tag.metadata()
        if metadata.hasKey("reviewTrack"):
            tag.metadata().setValue("tag.reviewTrack", track_name)
