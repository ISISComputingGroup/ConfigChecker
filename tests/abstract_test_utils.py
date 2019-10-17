import unittest
import six

from abc import ABCMeta, abstractmethod, abstractproperty
from settings import Settings
from util.channel_access import ChannelAccessUtils


@six.add_metaclass(ABCMeta)
class AbstractSingleTests(unittest.TestCase):
    """
    Abstract class for tests to be run exactly one regardless of how many components/configurations exist. It is meant
    to be extended by classes for configurations and for components.
    """

    # Create an abstract property (utils) than can be get and set and must be implemented by the implementing class
    @abstractproperty
    def utils(self):
        pass

    # Create an abstract property (type) than can be get and set and must be implemented by the implementing class
    @abstractproperty
    def type(self):
        pass

    def test_GIVEN_an_instrument_THEN_all_block_pvs_are_interesting(self):
        interesting_pvs = ChannelAccessUtils(Settings.pv_prefix).get_interesting_pvs()

        if len(interesting_pvs) == 0:
            self.skipTest("Set of interesting PVs is empty, this is probably because the instrument {} is off. Since "
                          "we do not know interesting pvs, {} are not checked for non interesting block pvs test is "
                          "terminated early.".format(Settings.name, self.type))

        non_interesting_block_pvs = [block_pv for block_pv in self.utils.get_set_of_block_pvs_for_all_configs(
                                        ) if block_pv not in interesting_pvs]
        num_non_interesting_block_pvs = len(non_interesting_block_pvs)

        if num_non_interesting_block_pvs != 0:
            print("\nWARNING! The instrument {} has {} non-interesting pvs that have a block on them in {}".
                  format(Settings.pv_prefix, len(non_interesting_block_pvs), self.type))
            self.update_total_non_interesting_block_pvs(num_non_interesting_block_pvs)
            print(non_interesting_block_pvs)

    @abstractmethod
    def update_total_non_interesting_block_pvs(self, num_non_interesting_block_pvs):
        """
        This method should monitor the number of non interesting block pvs discovered so far for
        components/configurations and print it to the screen.
        :param num_non_interesting_block_pvs: the number of non interesting block pvs for all instruments so far.
        """
        pass