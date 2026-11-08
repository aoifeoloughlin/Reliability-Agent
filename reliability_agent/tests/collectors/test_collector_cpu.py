import pytest

class TestCollectorCpu:

    def test_initialisation(self):
        # both samples are None

    def test_read_proc_stat(self):
        # Retrieves and stores two CPU samples with a one-second interval.

    def test_calculate_total_cpu_time(self):
        # verifies the total cpu time calculations

    def test_calculate_idle_cpu_time(self):
        # verifies the idle cpu time calculations
    
    def test_calculate_cpu_percentage(self):
        # verifies the cpu percentage calculations

    def test_zero_cpu_time(self):
        # verifies the catch if there is zero cpu or invalid

    def test_collect(self):
        # verifies collect returns something

    def test_collection_handles_missing_cpu_fields(self):
        # when the stats are missing fields

    def test_collection_handles_psutil_exception(self):
        # verifies something with step in if there is a collection fail from psutil

    def test_repeated_collection(self):
        # verifies multiple cycles of collection
    
    
