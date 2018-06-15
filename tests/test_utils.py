# -*- coding: UTF-8 -*-
#!/usr/bin/env python

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import environ
from six import string_types as str
from sys import exit
import unittest
from six.moves.urllib.parse import urlparse
import xml.etree.ElementTree as ET

# module target
from modules import isogeo2office_utils


# #############################################################################
# ########## Classes ###############
# ##################################


class Search(unittest.TestCase):
    """Test utils functions of Isogeo to Office."""

    # standard methods
    def setUp(self):
        # """Executed before each test."""
        self.utils = isogeo2office_utils()

    def tearDown(self):
        """Executed after each test."""
        pass

    #  -- Openers ------------------------------------------------------------
    def test_url_opener(self):
        """Test URL opener"""
        self.utils.open_urls(["https://www.isogeo.com", ])
        self.utils.open_urls(["https://www.isogeo.com",
                              "https://github.com/isogeo/isogeo-2-office"])

    def test_dirfile_opener_ok(self):
        """Test file/folder opener"""
        self.utils.open_dir_file(r"modules")

    def test_dirfile_opener_bad(self):
        """Test file/folder opener"""
        with self.assertRaises(IOError):
            self.utils.open_dir_file(r"toto")

    #  -- Cleaners ------------------------------------------------------------
    def test_clean_accents(self):
        """Test special characters remover"""
        # set
        in_str = "Spécial $#! caractères n'ont que des esp@ces à droite 888323"
        # run
        clean_stripped_accent = self.utils.clean_special_chars(in_str)
        clean_underscored_accent = self.utils.clean_special_chars(in_str, "_")
        clean_stripped_pure = self.utils.clean_special_chars(in_str, accents=0)
        clean_underscored_pure = self.utils.clean_special_chars(in_str, "_", accents=0)
        # check
        self.assertEqual(clean_stripped_accent,
                         "Spécialcaractèresnontquedesespcesàdroite888323")
        self.assertEqual(clean_underscored_accent,
                         "Spécial_caractères_n_ont_que_des_esp_ces_à_droite_888323")
        self.assertEqual(clean_stripped_pure,
                         "Spcialcaractresnontquedesespcesdroite888323")
        self.assertEqual(clean_underscored_pure,
                         "Sp_cial_caract_res_n_ont_que_des_esp_ces_droite_888323")

    def test_clean_filename_ok(self):
        """Test clean filenames"""
        # set
        in_filename = "mon rapport de catalogage super cool ! .zip"
        # run
        filename_soft = self.utils.clean_filename(in_filename, mode="soft")
        filename_strict = self.utils.clean_filename(in_filename, mode="strict")
        # check
        self.assertEqual(filename_soft,
                         "mon rapport de catalogage super cool ! .zip")
        self.assertEqual(filename_strict,
                         "mon rapport de catalogage super cool  .zip")

    def test_clean_filename_bad(self):
        """Test filenames errors"""
        with self.assertRaises(ValueError):
            self.utils.clean_filename(r"toto", mode="youpi")

    def test_clean_xml(self):
        """Test XML cleaner"""
        # set
        in_xml = """<field name="id">abcdef</field>
                    <field name="intro" > pqrst</field>
                    <field name="desc"> this is a test file. We will show 5>2 and 3<5 and
                    try to remove non xml compatible characters.</field>
                 """
        # run
        clean_xml_soft = self.utils.clean_xml(in_xml)
        clean_xml_strict = self.utils.clean_xml(in_xml, mode="strict")
        # check
        ET.fromstring("<root>{}</root>".format(clean_xml_soft))
        ET.fromstring("<root>{}</root>".format(clean_xml_strict))
