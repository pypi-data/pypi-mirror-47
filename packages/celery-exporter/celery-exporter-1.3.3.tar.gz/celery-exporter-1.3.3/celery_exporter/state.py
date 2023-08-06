import threading
from operator import itemgetter
from itertools import chain

from celery.states import READY_STATES, RECEIVED
from celery.utils.functional import LRUCache
from celery.events.state import Task, TASK_EVENT_TO_STATE

CELERY_DEFAULT_QUEUE = "celery"
CELERY_MISSING_DATA = "undefined"


class CeleryState:
    event_count = 0
    task_count = 0

    def __init__(self, max_tasks_in_memory=10000):
        self.tasks = LRUCache(max_tasks_in_memory)
        self._queue_by_task = {}
        self._mutex = threading.Lock()

    @classmethod
    def _gen_wildcards(self, name):
        chunked = name.split(".")
        res = [name]
        for elem in reversed(chunked):
            chunked.pop()
            res.append(".".join(chunked + ["*"]))
        return res

    @classmethod
    def get_config(self, app):
        res = dict()
        try:
            registered_tasks = app.control.inspect().registered_tasks().values()
            confs = app.control.inspect().conf()
        except Exception:  # pragma: no cover
            return res

        for task_name in set(chain.from_iterable(registered_tasks)):
            for conf in confs.values():
                default = conf.get("task_default_queue", CELERY_DEFAULT_QUEUE)
                if task_name in res and res[task_name] != default:
                    break

                task_wildcard_names = self._gen_wildcards(task_name)
                if "task_routes" in conf:
                    routes = conf["task_routes"]
                    res[task_name] = default
                    for i in task_wildcard_names:
                        if i in routes and "queue" in routes[i]:
                            res[task_name] = routes[i]["queue"]
                            break
                else:
                    res[task_name] = default
        return res

    def _measure_latency(self, evt):
        try:
            prev_evt = self.tasks[evt["uuid"]]
        except KeyError:  # pragma: no cover
            pass
        else:
            if prev_evt.state == RECEIVED:
                return evt["local_received"] - prev_evt.local_received

        return None

    def latency(self, evt):
        group, _, subject = evt["type"].partition("-")
        if group == "task":
            if subject == "started":
                return self._measure_latency(evt)
        return None

    def _event(self, evt, subject):
        tfields = itemgetter("uuid", "hostname", "timestamp", "local_received", "clock")
        get_task = self.tasks.__getitem__
        self.event_count += 1

        (uuid, hostname, timestamp, local_received, clock) = tfields(evt)
        is_client_event = subject == "sent"
        try:
            task, task_created = get_task(uuid), False
        except KeyError:
            task = self.tasks[uuid] = Task(uuid, cluster_state=None)
            task_created = True
        if is_client_event:
            task.client = hostname

        if subject == "received":
            self.task_count += 1

        task.event(subject, timestamp, local_received, evt)

        name = task.name
        if name is not None and "queue" in evt:
            if not name in self._queue_by_task:
                self._queue_by_task[name] = evt["queue"]

        return (task, task_created), subject

    def event(self, evt, subject):
        with self._mutex:
            return self._event(evt, subject)

    def collect(self, evt):
        group, _, subject = evt["type"].partition("-")
        runtime = None
        if group == "task":
            state = TASK_EVENT_TO_STATE[subject]
            if state in READY_STATES:
                try:
                    with self._mutex:
                        name = self.tasks.pop(evt["uuid"]).name or CELERY_MISSING_DATA
                except (KeyError):  # pragma: no cover
                    name = CELERY_MISSING_DATA
                finally:
                    queue = self._queue_by_task.get(name, CELERY_MISSING_DATA)
                    if "runtime" in evt:
                        runtime = evt["runtime"]
                    return (name, state, runtime, queue)
            else:
                self.event(evt, subject)
                try:
                    name = self.tasks[evt["uuid"]].name or CELERY_MISSING_DATA
                except (KeyError):  # pragma: no cover
                    name = CELERY_MISSING_DATA
                finally:
                    queue = self._queue_by_task.get(name, CELERY_MISSING_DATA)
                    return (name, state, runtime, queue)
        return (None, None, None, None)
