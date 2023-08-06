import os
from yggdrasil.examples.tests import TestExample


class TestExampleGS3(TestExample):
    r"""Test the Getting Started Lesson 3 example."""

    example_name = 'gs_lesson3'

    @property
    def input_files(self):
        r"""Input file."""
        return [os.path.join(self.yamldir, 'Input', 'input.txt')]

    @property
    def output_files(self):
        r"""Output file."""
        return [os.path.join(self.yamldir, 'output.txt')]
