from collections import defaultdict

class Stats:
    """
    Have to figure out whether to merge all these classes together.
    Essentially, some of these would be updating themselves in real-time while
    others I am not entirely sure about. System stress for real-time statistics
    is something I need to figure out here.
    """

    def __init__(self, connection):
        self.info = connection.info()

    def _stats(self):
        """
        Mirrors the Stats section from Redis INFO
        """
        db_stats = defaultdict(int)

        db_stats['connections_received'] = self.info['total_connections_received']
        db_stats['commands_processed'] = self.info['total_commands_processed']
        db_stats['net_input_bytes'] = self.info['total_net_input_bytes']
        db_stats['net_output_bytes'] = self.info['total_net_output_bytes']
        db_stats['rejected_connections'] = self.info['rejected_connections']

        return db_stats

    def print_stats(self):
        "prints the results from the stats function"
        return {**self._stats()}