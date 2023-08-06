from cloudshell.devices.flows.cli_action_flows import ShutdownFlow
from cloudshell.networking.juniper.cli.juniper_cli_handler import JuniperCliHandler
from cloudshell.networking.juniper.command_actions.system_actions import SystemActions


class JuniperShutdownFlow(ShutdownFlow):
    def __init__(self, cli_handler, logger):
        """
          Enable snmp flow
          :param cli_handler:
          :type cli_handler: JuniperCliHandler
          :param logger:
          :return:
          """
        super(JuniperShutdownFlow, self).__init__(cli_handler, logger)
        self._cli_handler = cli_handler

    def execute_flow(self):
        with self._cli_handler.default_mode_service() as cli_service:
            system_actions = SystemActions(cli_service, self._logger)
            return system_actions.shutdown()
