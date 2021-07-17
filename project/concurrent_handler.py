from asyncio import Queue, wait, FIRST_COMPLETED, create_task

class ConcurrentHandler:
    """
    Concurrently handle multiple tasks
    
    Creates a handler for a number of tasks that need to be looped,
    run in parallel and cancelled based on certain rules.
    """

    def __init__(self, tasks):
        """
        Parameters
        ----------

            tasks : dict
                a dictionary of async functions to run
        """
        self._tasks = tasks
        self._pending = {key: None for key in tasks.keys()}

    async def process(self):
        """
        Run a single iteration of each of the tasks

        This will resume unfinished tasks, and spin up
        new ones for those that have completed
        """
        (done, pending) = await wait([
            existing_task if existing_task is not None else create_task(self._tasks[name](), name=name)
            for (name, existing_task)
            in self._pending.items()
        ], return_when=FIRST_COMPLETED)

        self._pending = {key: None for key in self._tasks.keys()}

        # If one of our tasks has an exception, we probably want to re-raise it
        exceptions = [
            (item, ex) for (item, ex) in [(item.get_name(), item.exception()) for item in done]
            if ex is not None
        ]
        if len(exceptions) > 0:
            [item.cancel() for item in pending]
            raise Exception(f"Tasks failed - {exceptions}")

        # Get our existing messages ready to requeue
        for item in pending:
            self._pending = {
                **self._pending,
                item.get_name(): item
            }
