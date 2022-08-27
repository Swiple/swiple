class SchedulerInterface:
    def start(self) -> None:
        """Starts scheduler if required."""

    def shutdown(self) -> None:
        """Shutdown scheduler if required."""

    def add_schedule(self, *args):
        """Adds a schedule to scheduler job store."""

    def modify_schedule(self, *args):
        """Modifies an existing schedule."""

    def pause_schedule(self, *args):
        """Pauses schedule."""

    def resume_schedule(self, *args):
        """Resumes scheduler."""

    def remove_schedule(self, *args):
        """Removes a schedule base on a schedule_id."""

    def get_schedule(self, *args):
        """Returns a schedule base on a schedule_id."""

    def list_schedules(self, *args):
        """Returns a list of schedules as dicts."""

    def to_dict(self, *args):
        """Schedule object to a dictionary."""

    def delete_by_dataset(self, *args):
        """Deletes all schedules with a particular dataset_id."""

    def delete_by_datasource(self, *args):
        """Deletes all schedules with a particular datasource_id."""

    def next_schedule_run_times(self, *args):
        """Returns a list of the upcoming schedule datetimes based on schedule inputs."""
