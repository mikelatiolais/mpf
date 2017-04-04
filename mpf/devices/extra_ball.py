"""Device that implements an extra ball."""
from mpf.core.mode import Mode
from mpf.core.mode_device import ModeDevice
from mpf.core.player import Player


class ExtraBall(ModeDevice):

    """An extra ball which can be awarded once per player."""

    config_section = 'extra_balls'
    collection = 'extra_balls'
    class_label = 'extra_ball'

    def __init__(self, machine, name):
        """Initialise extra ball."""
        super().__init__(machine, name)
        self.player = None
        self.group = None
        self._enabled = False

    def _initialize(self):

        super()._initialize()

        self.group = self.config['group']

        try:
            self.group.extra_ball_initialized(self)
        except AttributeError:
            pass

        if self.config['enabled']:
            self._enabled = True

    def award(self, **kwargs):
        """Award extra ball to player if enabled."""
        del kwargs

        if not self.player or not self._enabled:
            return

        if (self.config['max_per_game'] and
                self.player['extra_ball_{}_awarded'.format(self.name)] <
                self.config['max_per_game']):

            if self.group and not self.group.ok_to_award_eb():
                return

            self.player['extra_ball_{}_awarded'.format(self.name)] += 1
            self.player.extra_balls += 1

            # still need to send this even if EBs are disabled since we want
            # to post the disabled event
            self.group.award()

    def light(self, **kwargs):
        del kwargs

        if not self.player:
            return

        self.machine.extra_ball_controller.light()

    def reset(self, **kwargs):
        """Reset extra ball.

        Does not reset the additional ball the player received. Only resets the device and allows to award another
        extra ball to the player.
        """
        del kwargs

        if not self.player:
            return

        self.player.extra_balls_awarded[self.name] = 0

    def device_added_to_mode(self, mode: Mode, player: Player):
        """Load extra ball in mode and initialise player.

        Args:
            mode: Mode which is loaded
            player: Current player
        """
        super().device_added_to_mode(mode, player)
        self.player = player

        if not player.is_player_var('extra_ball_{}_awarded'.format(self.name)):
            player['extra_ball_{}_awarded'.format(self.name)] = 0

        '''player_var: extra_ball_(name)_awarded

        desc: The number of times this extra ball has been awarded to the
        player in this game. Note that the default max is one (meaning that
        each extra ball can be awarded once per game), so this value will only
        be 0 or 1 unless you change the max setting for this extra ball.'''

    def device_removed_from_mode(self, mode: Mode):
        """Unload extra ball.

        Args:
            mode: Mode which is unloaded
        """
        del mode
        self.player = None
