

class SchedulerInterface:
    def start(self) -> None:
        """Starts scheduler if required."""
        pass

    def shutdown(self) -> None:
        """Shutdown scheduler if required."""
        pass
    
    def add_schedule(self, *args):
        """Adds a schedule to scheduler job store."""
        pass

    def modify_schedule(self, *args):
        """Modifies an existing schedule."""
        pass

    def pause_schedule(self, *args):
        """Pauses schedule."""
        pass

    def resume_schedule(self, *args):
        """Resumes scheduler."""
        pass

    def remove_schedule(self, *args):
        """Removes a schedule base on a schedule_id."""
        pass

    def get_schedule(self, *args):
        """Returns a schedule base on a schedule_id."""
        pass

    def list_schedules(self, *args):
        """Returns a list of schedules as dicts."""
        pass

    def to_dict(self, *args):
        """Schedule object to a dictionary."""
        pass

    def delete_by_dataset(self, *args):
        """Deletes all schedules with a particular dataset_id."""
        pass

    def delete_by_datasource(self, *args):
        """Deletes all schedules with a particular datasource_id."""
        pass

    def next_schedule_run_times(self, *args):
        """Returns a list of the upcoming schedule datetimes based on schedule inputs."""
        pass
