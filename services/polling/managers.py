import logging
import os
from typing import Type

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from services.polling.jobs import BaseJob, PlayerSyncJob

log = logging.getLogger(__name__)


class SchedulerService(AsyncIOScheduler):
    _default_job_opts = dict(
        max_instances=1_000_000,
        coalesce=False,
        misfire_grace_time=None,
        replace_existing=True,
    )

    def start(self) -> None:
        run_main = os.environ.get("RUN_MAIN") == "true"
        is_reload = os.environ.get("UVICORN_RELOAD") == "true"
        if is_reload and not run_main:
            log.error("Skipping scheduler in reloader process.")
            return

        if self.running:
            raise RuntimeError("Coś się tobie pomyliło chłopie, scheduler już działa, popraw kod!")

        super().start()
        log.error("SchedulerService started")
        self.add_job(PlayerSyncJob)

    def shutdown(self) -> None:
        if not self.running:
            raise RuntimeError(
                "Coś się tobie pomyliło chłopie, scheduler już nie działa, popraw kod!"
            )

        super().shutdown(wait=False)
        log.error("SchedulerService stopped")

    def add_job(self, job_cls: Type[BaseJob], **kwargs) -> None:
        job: BaseJob = job_cls()
        trigger: IntervalTrigger = job.build_trigger()

        # kwargs gonna override default options if provided :)
        super().add_job(job.run, trigger=trigger, id=job.job_id, **self._default_job_opts, **kwargs)
        log.error(f"Registered job {job.job_id}")

    def reschedule_job(self, job_id: str, trigger: IntervalTrigger) -> None:
        super().reschedule_job(job_id, trigger)
        log.error(f"Rescheduled job {job_id}")


scheduler = SchedulerService()
