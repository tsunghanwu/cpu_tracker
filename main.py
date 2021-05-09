from tracker import Tracker

tracker = Tracker(pid=1506)
tracker.track(interval=2, time_span=1)
tracker.save()
tracker.plot()

