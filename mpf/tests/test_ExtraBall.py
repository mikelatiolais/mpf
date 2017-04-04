from mpf.tests.MpfTestCase import MpfTestCase


class TestExtraBall(MpfTestCase):

    def getConfigFile(self):
        return 'config.yaml'

    def getMachinePath(self):
        return 'tests/machine_files/extra_ball/'

    def get_platform(self):
        return 'smart_virtual'

    def _start_game(self):
        # prepare game
        self.machine.switch_controller.process_switch('s_ball_switch1', 1)
        self.machine.switch_controller.process_switch('s_ball_switch2', 1)
        self.advance_time_and_run(10)
        self.assertEqual(2, self.machine.ball_controller.num_balls_known)
        self.assertEqual(2, self.machine.ball_devices.bd_trough.balls)

        # start game
        self.machine.switch_controller.process_switch('s_start', 1)
        self.machine.switch_controller.process_switch('s_start', 0)
        self.machine_run()

    def _add_second_player(self):
        # add second player
        self.machine.switch_controller.process_switch('s_start', 1)
        self.machine.switch_controller.process_switch('s_start', 0)
        self.machine_run()

        self.assertEqual(2, len(self.machine.game.player_list))

    def test_extra_ball(self):
        self._start_game()
        self._add_second_player()

        # start mode
        self.post_event("start_mode1")

        # mode loaded. ball_lock2 should be enabled
        self.assertTrue(self.machine.extra_balls.test_extra_ball)
        self.assertTrue(self.machine.extra_balls.test_extra_ball.player)
        self.assertEqual(1, self.machine.game.player.number)
        self.assertEqual(0, self.machine.game.player.extra_ball_test_extra_ball_awarded)
        self.assertEqual(0, self.machine.game.player.extra_balls)

        # stop mode
        self.post_event("stop_mode1")

        # nothing should happen
        self.post_event("test_extra_ball_award")
        self.assertEqual(1, self.machine.game.player.number)
        self.assertEqual(0, self.machine.game.player.extra_ball_test_extra_ball_awarded)
        self.assertEqual(0, self.machine.game.player.extra_balls)
        self.assertFalse(self.machine.extra_balls.test_extra_ball.player)

        # start mode (again)
        self.post_event("start_mode1")

        self.assertTrue(self.machine.extra_balls.test_extra_ball)
        self.assertTrue(self.machine.extra_balls.test_extra_ball.player)
        self.assertEqual(1, self.machine.game.player.number)
        self.assertEqual(0, self.machine.game.player.extra_ball_test_extra_ball_awarded)
        self.assertEqual(0, self.machine.game.player.extra_balls)

        # player get extra_ball
        self.post_event("test_extra_ball_award")
        self.assertEqual(1, self.machine.game.player.number)
        self.assertEqual(1, self.machine.game.player.ball)
        self.assertEqual(1, self.machine.game.player.extra_ball_test_extra_ball_awarded)
        self.assertEqual(1, self.machine.game.player.extra_balls)

        # but only once
        self.post_event("test_extra_ball_award")
        self.assertEqual(1, self.machine.game.player.number)
        self.assertEqual(1, self.machine.game.player.ball)
        self.assertEqual(1, self.machine.game.player.extra_ball_test_extra_ball_awarded)
        self.assertEqual(1, self.machine.game.player.extra_balls)

        # reset the extra ball
        self.post_event("test_extra_ball_reset")

        # should give another extra ball
        self.post_event("test_extra_ball_award")
        self.assertEqual(1, self.machine.game.player.number)
        self.assertEqual(1, self.machine.game.player.ball)
        self.assertEqual(1, self.machine.game.player.extra_ball_test_extra_ball_awarded)
        self.assertEqual(2, self.machine.game.player.extra_balls)

        # takes roughly 4s to get ball confirmed
        self.advance_time_and_run(4)
        self.assertNotEqual(None, self.machine.game)
        self.assertEqual(1, self.machine.playfield.balls)

        # ball drains right away
        self.machine.switch_controller.process_switch('s_ball_switch1', 1)
        self.machine.switch_controller.process_switch('s_ball_switch2', 1)
        self.advance_time_and_run(1)

        self.assertEqual(1, self.machine.game.player.number)
        self.assertEqual(1, self.machine.game.player.ball)
        self.assertEqual(True, self.machine.game.player.extra_balls_awarded['test_extra_ball'])
        self.assertEqual(1, self.machine.game.player.extra_balls)

        # takes roughly 4s to get ball confirmed
        self.advance_time_and_run(4)
        self.assertNotEqual(None, self.machine.game)
        self.assertEqual(1, self.machine.playfield.balls)

        # ball drains right away
        self.machine.switch_controller.process_switch('s_ball_switch1', 1)
        self.machine.switch_controller.process_switch('s_ball_switch2', 1)
        self.advance_time_and_run(1)

        # takes roughly 4s to get ball confirmed
        self.advance_time_and_run(4)
        self.assertNotEqual(None, self.machine.game)
        self.assertEqual(1, self.machine.playfield.balls)

        # ball drains right away
        self.machine.switch_controller.process_switch('s_ball_switch1', 1)
        self.machine.switch_controller.process_switch('s_ball_switch2', 1)
        self.advance_time_and_run(1)

        # start mode
        self.post_event("start_mode1")

        self.assertEqual(2, self.machine.game.player.number)
        self.assertEqual(1, self.machine.game.player.ball)
        self.assertEqual(False, self.machine.game.player.extra_balls_awarded['test_extra_ball'])
        self.assertEqual(0, self.machine.game.player.extra_balls)

        # game should not end
        self.assertNotEqual(None, self.machine.game)
        self.assertEqual(0, self.machine.playfield.balls)

        # game should eject another ball
        self.advance_time_and_run(4)
        self.assertNotEqual(None, self.machine.game)
        self.assertEqual(1, self.machine.playfield.balls)

        # ball drains also
        self.machine.switch_controller.process_switch('s_ball_switch1', 1)
        self.machine.switch_controller.process_switch('s_ball_switch2', 1)

        # game should end
        self.advance_time_and_run(1)
        self.assertEqual(None, self.machine.game)

    def test_global_max_per_game(self):
        self.machine.config['global_extra_ball_settings']['max_per_game'] = 2

        self._start_game()
        self.post_event('start_mode1')

        self.post_event('light_eb1')
        self.post_event('light_eb2')
        self.post_event('light_eb3')

        self.post_event('award_lit_extra_ball')
        self.post_event('award_lit_extra_ball')
        self.post_event('award_lit_extra_ball')

        self.assertEqual(self.machine.game.player.extra_balls, 2)

    def test_max_per_ball(self):
        self.machine.config['global_extra_ball_settings']['max_per_ball'] = 1

    def test_max_lit(self):
        self.machine.config['global_extra_ball_settings']['max_lit'] = 1

    def test_lit_memory_true(self):
        pass

    def test_lit_memory_false(self):
        self.machine.config['global_extra_ball_settings']['lit_memory'] = False

    def test_events_only(self):
        self.machine.config['global_extra_ball_settings']['events_only'] = True

    def test_eb_max_per_game(self):
        # eb1 max_per_game = 2, others = 1
        pass

    # todo add light events to general test
