"""Unit test for rules.py."""

import xml.etree.ElementTree as ET

from absl.testing import absltest
from election_results_xml_validator import base
from election_results_xml_validator.rules import PercentSum
from election_results_xml_validator.rules import OnlyOneElection


class RulesTest(absltest.TestCase):

  def setUp(self):
    super(RulesTest, self).setUp()
    self.percent_sum = PercentSum(None, None)
    self.only_one_election = OnlyOneElection(None, None)

  def testZeroPercents(self):
    root_string = """
    <Contest>
      <BallotSelection>
        <VoteCountsCollection>
          <VoteCounts>
            <OtherType>total-percent</OtherType>
            <Count>0.0</Count>
          </VoteCounts>
          <VoteCounts>
            <OtherType>total-percent</OtherType>
            <Count>0.0</Count>
          </VoteCounts>
        </VoteCountsCollection>
      </BallotSelection>
    </Contest>
    """

    self.percent_sum.check(ET.fromstring(root_string))

  def testHundredPercents(self):
    root_string = """
    <Contest>
      <BallotSelection>
        <VoteCountsCollection>
          <VoteCounts>
            <OtherType>total-percent</OtherType>
            <Count>60.0</Count>
          </VoteCounts>
          <VoteCounts>
            <OtherType>total-percent</OtherType>
            <Count>40.0</Count>
          </VoteCounts>
        </VoteCountsCollection>
      </BallotSelection>
    </Contest>
    """

    self.percent_sum.check(ET.fromstring(root_string))

  def testInvalidPercents_fails(self):
    root_string = """
    <Contest>
      <BallotSelection>
        <VoteCountsCollection>
          <VoteCounts>
            <OtherType>total-percent</OtherType>
            <Count>60.0</Count>
          </VoteCounts>
          <VoteCounts>
            <OtherType>total-percent</OtherType>
            <Count>20.0</Count>
          </VoteCounts>
        </VoteCountsCollection>
      </BallotSelection>
    </Contest>
    """

    with self.assertRaises(base.ElectionError):
      self.percent_sum.check(ET.fromstring(root_string))

  def testExactlyOneElection(self):
    root_string = """
    <ElectionReport>
      <Election></Election>
    </ElectionReport>
    """

    self.only_one_election.check(ET.fromstring(root_string))

  def testMoreThanOneElection_fails(self):
    root_string = """
    <ElectionReport>
      <Election></Election>
      <Election></Election>
    </ElectionReport>
    """

    with self.assertRaises(base.ElectionError):
      self.only_one_election.check(ET.fromstring(root_string))


if __name__ == '__main__':
  absltest.main()
