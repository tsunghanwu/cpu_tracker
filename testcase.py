from tracker import Tracker

tracker = Tracker(pid=5791)
tracker.track(interval=10, time_span=1)
tracker.save()
tracker.plot()

