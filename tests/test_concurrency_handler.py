from unittest import IsolatedAsyncioTestCase
from project.concurrent_handler import ConcurrentHandler
from asyncio import Event


class TestConcurrentHandler(IsolatedAsyncioTestCase):
    async def test_process_no_tasks(self):
        """
        If I have no tasks, there should be none left in pending
        """
        handler = ConcurrentHandler({})
        await handler.process()
        self.assertEqual(handler._pending, {})

    async def test_process_completed_tasks(self):
        """
        If my tasks complete, they should not sit in pending
        """

        async def instant_task():
            pass

        handler = ConcurrentHandler({"task1": instant_task, "task2": instant_task})
        await handler.process()
        self.assertEqual(handler._pending, {"task1": None, "task2": None})

    async def test_non_completed_task(self):
        """
        If a task doesn't complete, it should be popped in the queue
        """
        event = Event()

        async def instant_task():
            pass

        async def waiting_task():
            nonlocal event
            await event.wait()

        handler = ConcurrentHandler({"task1": instant_task, "task2": waiting_task})
        await handler.process()
        self.assertEqual(set(handler._pending.keys()), {"task1", "task2"})
        self.assertEqual(handler._pending["task1"], None)
        self.assertNotEqual(handler._pending["task2"], None)

    async def test_reflow_tasks(self):
        """
        If a task completes after going into pending, it should clear out
        after the next process
        """
        event = Event()

        async def instant_task():
            pass

        async def waiting_task():
            nonlocal event
            await event.wait()

        handler = ConcurrentHandler({"task1": instant_task, "task2": waiting_task})
        await handler.process()
        event.set()
        await handler.process()
        self.assertEqual(handler._pending, {"task1": None, "task2": None})
