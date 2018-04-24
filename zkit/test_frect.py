from unittest import TestCase

from pygame import Rect

from zkit.frect import FRect

class FRectTestCase(TestCase):

    def test_accessors(self):
        rect = Rect(10, 12, 14, 16)
        frect = FRect(rect)

        self.assertEqual(frect.x, rect.x)
        self.assertEqual(frect.topleft, rect.topleft)
