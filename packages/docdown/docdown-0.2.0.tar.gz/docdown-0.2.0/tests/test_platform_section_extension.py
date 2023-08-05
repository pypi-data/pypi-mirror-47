# -*- coding: utf-8 -*-

"""
test_note_blocks_extension
----------------------------------

Tests for `docdown.note_blocks` module.
"""

from __future__ import absolute_import, print_function, unicode_literals

import unittest

import markdown


class PlatformSectionExtensionTest(unittest.TestCase):
    """
    Integration test with markdown for :class:`docdown.platform_section.PlatformSectionExtension`
    """
    MARKDOWN_EXTENSIONS = ['docdown.platform_section']

    def build_config_for_platform_section(self, section):
        return {
            'docdown.platform_section': {
                'platform_section': section,
            }
        }

    def test_section_does_not_match(self):
        text = ('@![asdf]\n'
                'some content\nnot shown\n\n'
                '!@')

        html = markdown.markdown(
            text,
            extension_configs=self.build_config_for_platform_section('Android'),
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = ''
        self.assertEqual(expected_output, html)

    def test_section_does_match(self):
        text = ('@![asdf]\n'
                'some content\nshown\n\n'
                '!@ \n')

        html = markdown.markdown(
            text,
            extension_configs=self.build_config_for_platform_section('asdf'),
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '<p>some content\nshown</p>'
        self.assertEqual(expected_output, html)

    def test_section_markdown_case_insensitive(self):
        text = ('@![ASDF]\n'
                'some content\nshown\n\n'
                '!@\n')

        html = markdown.markdown(
            text,
            extension_configs=self.build_config_for_platform_section('asdf'),
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '<p>some content\nshown</p>'
        self.assertEqual(expected_output, html)

    def test_section_config_case_insensitive(self):
        text = ('@![asdf]\n'
                'some content\nshown\n\n'
                '!@ \n')

        html = markdown.markdown(
            text,
            extension_configs=self.build_config_for_platform_section('ASDF'),
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '<p>some content\nshown</p>'
        self.assertEqual(expected_output, html)

    def test_multiple_platforms_section(self):
        text = ('@![asdf,QwErTy]\n'
                'some content\nshown\n\n'
                '!@\n')

        html = markdown.markdown(
            text,
            extension_configs=self.build_config_for_platform_section('qwerty'),
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '<p>some content\nshown</p>'
        self.assertEqual(expected_output, html)

    def test_multiple_sections(self):
        text = ('@![asdf,QwErTy]\n'
                'some content\nnot shown\n\n'
                '!@\n'
                '\n'
                '@![zxcv]\n'
                'some content\nshown\n\n'
                '!@\n')

        html = markdown.markdown(
            text,
            extension_configs=self.build_config_for_platform_section('zxcv'),
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '<p>some content\nshown</p>'
        self.assertEqual(expected_output, html)

    def test_multiple_sections_with_code_snippet(self):
        text = ('@![iOS]\n'
                'some iOS content not shown\n\n'
                '!@\n'
                '\n'
                '@![Android]\n'
                'some Android content shown\n\n'
                '``` java\n'
                'String java = "asdf";\n'
                '```\n'
                '!@\n')

        html = markdown.markdown(
            text,
            extension_configs=self.build_config_for_platform_section('Android'),
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '<p>some Android content shown</p>\n<p>``` java\nString java = "asdf";</p>'
        self.assertEqual(expected_output, html)
