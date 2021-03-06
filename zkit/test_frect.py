"""
Test both floating point and integer properties on the FRect class
"""

from unittest import TestCase
from collections import namedtuple

from zkit.frect import FRect as Rect


class RectTests(TestCase):

    def setUp(self):
        self.r = Rect(11, 12, 13, 14)

    def test_iter(self):
        expected = [self.r.left, self.r.top,
                    self.r.width, self.r.height]
        expected.reverse()
        for i in self.r:
            self.assertEqual(expected.pop(), i)
        self.assertEqual(len(expected), 0)

    def test_index(self):
        """can index the rect as a list"""
        rekt = [self.r[i] for i in range(len(self.r))]
        self.assertEqual(rekt, [self.r.left, self.r.top,
                                self.r.width, self.r.height])

    def test_index_raises_index_error(self):
        with self.assertRaises(IndexError):
            self.r[10]

    def test_equality(self):
        r0 = Rect(10, 11, 12, 13)
        r1 = Rect(10, 11, 12, 13)
        r2 = Rect(0, 0, 0, 0)
        assert (r0 == r1)
        assert (not r0 == r2)

    def test_init_4_args(self):
        r = Rect(10, 11, 12, 13)
        self.assertEqual(r.left, 10)
        self.assertEqual(r.top, 11)
        self.assertEqual(r.width, 12)
        self.assertEqual(r.height, 13)

    def test_init_2_args(self):
        r = Rect((10, 11), (12, 13))
        self.assertEqual(r.left, 10)
        self.assertEqual(r.top, 11)
        self.assertEqual(r.width, 12)
        self.assertEqual(r.height, 13)

    def test_init_object(self):
        RectLike = namedtuple("RectLike", "left, top, width, height")
        r = Rect(RectLike(10, 11, 12, 13))
        self.assertEqual(r.left, 10)
        self.assertEqual(r.top, 11)
        self.assertEqual(r.width, 12)
        self.assertEqual(r.height, 13)

    def test_init_bad_args(self):
        with self.assertRaisesRegex(ValueError, "Invalid"):
            Rect(1, 2, 3)

    def test_get_x(self):
        self.assertEqual(self.r.x, 11)

    def test_get_y(self):
        self.assertEqual(self.r.y, 12)

    def test_get_right(self):
        self.assertEqual(self.r.right, 24)

    def test_get_bottom(self):
        self.assertEqual(self.r.bottom, 26)

    def test_get_topleft(self):
        self.assertEqual((11, 12), self.r.topleft)

    def test_get_bottomleft(self):
        self.assertEqual((11, 26), self.r.bottomleft)

    def test_get_topright(self):
        self.assertEqual((24, 12), self.r.topright)

    def test_get_bottomright(self):
        self.assertEqual((24, 26), self.r.bottomright)

    def test_get_centerx(self):
        self.assertEqual(17, self.r.centerx)

    def test_get_centery(self):
        self.assertEqual(19, self.r.centery)

    def test_get_center(self):
        self.assertEqual((17, 19), self.r.center)

    def test_get_midtop(self):
        self.assertEqual((17, 12), self.r.midtop)

    def test_get_midleft(self):
        self.assertEqual((11, 19), self.r.midleft)

    def test_get_midbottom(self):
        self.assertEqual((17, 26), self.r.midbottom)

    def test_get_midright(self):
        self.assertEqual((24, 19), self.r.midright)

    def test_get_size(self):
        self.assertEqual((13, 14), self.r.size)

    def test_get_width(self):
        self.assertEqual(13, self.r.w)

    def test_get_height(self):
        self.assertEqual(14, self.r.height)

    def test_set_x(self):
        self.r.x = 12
        self.assertEqual(self.r.x, 12)

    def test_set_y(self):
        self.r.y = 13
        self.assertEqual(self.r.y, 13)

    def test_set_right(self):
        self.r.right = 28
        self.assertEqual(self.r.right, 28)

    def test_set_bottom(self):
        self.r.bottom = 27
        self.assertEqual(self.r.bottom, 27)

    def test_set_topleft(self):
        self.r.topleft = (13, 14)
        self.assertEqual((13, 14), self.r.topleft)

    def test_set_bottomleft(self):
        self.r.bottomleft = (12, 27)
        self.assertEqual((12, 27), self.r.bottomleft)

    def test_set_topright(self):
        self.r.topright = (25, 13)
        self.assertEqual((25, 13), self.r.topright)

    def test_set_bottomright(self):
        self.r.bottomright = 25, 27
        self.assertEqual((25, 27), self.r.bottomright)

    def test_set_centerx(self):
        self.r.centerx = 18
        self.assertEqual(18, self.r.centerx)

    def test_set_centery(self):
        self.r.centery = 20
        self.assertEqual(20, self.r.centery)

    def test_set_center(self):
        self.r.center = (18, 20)
        self.assertEqual((18, 20), self.r.center)

    def test_center_after_scale(self):
        self.r = Rect(0, 0, 1, 1)
        center = self.r.center
        new_center = self.r.scale(2, 2).center
        self.assertEqual((0, 0), center, new_center)

    def test_center_after_inflate(self):
        self.r = Rect(0, 0, 1, 1)
        center = self.r.center
        new_center = self.r.inflate(2, 2).center
        self.assertEqual((0, 0), center, new_center)

    def test_set_midtop(self):
        self.r.midtop = (18, 19)
        self.assertEqual((18, 19), self.r.midtop)

    def test_set_midleft(self):
        self.r.midleft = (12, 20)
        self.assertEqual((12, 20), self.r.midleft)

    def test_set_midbottom(self):
        self.r.midbottom = (18, 27)
        self.assertEqual((18, 27), self.r.midbottom)

    def test_set_midright(self):
        self.r.midright = (25, 20)
        self.assertEqual((25, 20), self.r.midright)

    def test_set_size(self):
        self.r.size = (14, 15)
        self.assertEqual((14, 15), self.r.size)

    def test_set_w(self):
        self.r.w = 14
        self.assertEqual(14, self.r.w)

    def test_set_h(self):
        self.r.h = 15
        self.assertEqual(15, self.r.h)

    def test_copy(self):
        r2 = self.r.copy()
        self.assertEqual(r2.topleft, self.r.topleft)
        self.assertEqual(r2.size, self.r.size)

    def test_move(self):
        x, y = self.r.topleft
        self.assertEqual((x + 10, y - 10), self.r.move(10, -10).topleft)

    def test_move_ip(self):
        x, y = self.r.topleft
        self.r.move_ip(10, -10)
        self.assertEqual((x + 10, y - 10), self.r.topleft)

    def test_clamp_too_big(self):
        r1 = Rect(50, 50, 50, 50)
        r2 = Rect(0, 0, 100, 100)
        center = r2.clamp(r1).center
        self.assertEqual(r1.center, center)

    def test_clamp_from_above(self):
        r1 = Rect(0, 0, 25, 25)
        r2 = Rect(0, 100, 100, 100)
        r3 = r1.clamp(r2)
        self.assertEqual(r3.topleft, (0, r2.top))

    def test_clamp_from_below(self):
        # equal
        r1 = Rect(0, 200, 25, 25)
        r2 = Rect(0, 100, 100, 100)
        r3 = r1.clamp(r2)
        self.assertEqual(r3.bottomleft, (0, r2.bottom))

        # greater
        r1 = Rect(0, 201, 25, 25)
        r2 = Rect(0, 100, 100, 100)
        r3 = r1.clamp(r2)
        self.assertEqual(r3.bottomleft, (0, r2.bottom))

    # "clamp from the left, clamp from the right you're the only rect
    # in sight!" -- Jimmy Buffet

    def test_clamp_from_the_left(self):
        r1 = Rect(0, 0, 25, 25)
        r2 = Rect(100, 0, 100, 100)
        r3 = r1.clamp(r2)
        self.assertEqual(r3.topleft, (r2.left, 0))

    def test_clamp_from_the_right(self):
        r1 = Rect(101, 0, 25, 25)
        r2 = Rect(0, 0, 100, 100)
        r3 = r1.clamp(r2)
        self.assertEqual(r3.topright, (r2.right, 0))

    def test_inflate(self):
        r = self.r.inflate(5, 5)
        self.assertEqual(r.center, self.r.center)
        self.assertEqual(r.size, (self.r.width + 5, self.r.height + 5))

    def test_scale(self):
        r = self.r.scale(2, 3)
        self.assertEqual(r.center, self.r.center)
        self.assertEqual(r.size, (self.r.width * 2, self.r.height * 3))

    def test_clip(self):
        # bigger
        r1 = Rect(0, 0, 125, 125)
        r2 = Rect(25, 25, 100, 100)
        self.assertEqual(r1.clip(r2).topleft, r2.topleft)
        self.assertEqual(r1.clip(r2).bottomright, r2.bottomright)

        # smaller
        r1 = Rect(0, 0, 75, 75)
        r2 = Rect(25, 25, 100, 100)
        self.assertEqual(r1.clip(r2).topleft, r2.topleft)
        self.assertEqual(r1.clip(r2).bottomright, r2.size)

    def test_union(self):
        r1 = Rect(0, 0, 50, 50)
        r2 = Rect(25, 25, 50, 50)
        r3 = r1.union(r2)
        self.assertEqual(r3.topleft, (0, 0))
        self.assertEqual(r3.bottomright, (75, 75))

    def test_unionall(self):
        r1 = Rect(0, 0, 50, 50)
        r2 = Rect(25, 25, 50, 50)
        r3 = Rect(50, 50, 50, 50)
        r4 = r1.unionall([r1, r2, r3])
        self.assertEqual(r4.topleft, (0, 0))
        self.assertEqual(r4.bottomright, (100, 100))

    def test_fit_wider(self):
        r1 = Rect(0, 0, 50, 50)
        r2 = Rect(0, 0, 75, 20)
        r3 = r1.fit(r2)
        self.assertEqual(r3.topleft, (27, 0))
        self.assertEqual(r3.size, (20, 20))

    def test_normalize(self):
        r1 = Rect(0, 0, -10, -10)
        r1.normalize()
        self.assertEqual(r1.topleft, (-10, -10))
        self.assertEqual(r1.size, (10, 10))

        r2 = Rect(0, 0, 10, 10)
        r2.normalize()
        self.assertEqual(r2.topleft, (0, 0))
        self.assertEqual(r2.size, (10, 10))

    def test_contains(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 3, 3)
        self.assertTrue(r1.contains(r2))
        self.assertFalse(r2.contains(r1))

    def test_collidepoint(self):
        r1 = Rect(0, 0, 15, 15)
        self.assertTrue(r1.collidepoint((10, 10)))
        self.assertFalse(r1.collidepoint((16, 10)))
        self.assertTrue(r1.collidepoint(10, 10))
        self.assertFalse(r1.collidepoint(16, 10))
        self.assertTrue(r1.collidepoint(10, 11, 12))

    def test_colliderect(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(20, 20, 10, 10)
        self.assertTrue(r1.colliderect(r2))
        self.assertTrue(r2.colliderect(r1))
        self.assertFalse(r1.colliderect(r3))
        self.assertFalse(r3.colliderect(r2))

    def test_collidelist(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(20, 20, 10, 10)
        r4 = Rect(25, 25, 10, 10)
        r5 = Rect(100, 100, 100, 100)
        rects = [r4, r3, r2]
        self.assertEqual(2, r1.collidelist(rects))
        self.assertEqual(-1, r5.collidelist(rects))

    def test_collidelistall(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(8, 8, 10, 10)
        r4 = Rect(25, 25, 10, 10)
        r5 = Rect(9, 9, 100, 100)
        rects = [r4, r3, r2, r5]
        self.assertEqual(r1.collidelistall(rects), [1, 2, 3])

    def test_collidedict(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(8, 8, 10, 10)
        r4 = Rect(25, 25, 10, 10)
        r5 = Rect(100, 100, 100, 100)
        rects = {"first": r1,
                 "second": r2,
                 "third": r3,
                 "fourth": r4}
        key, rect = r1.collidedict(rects)
        self.assertIn(key, rects)
        self.assertIn(rect, rects.values())
        self.assertNotEqual(id(rect), id(r1))
        self.assertEqual(r5.collidedict(rects), None)
        self.assertEqual(r1.collidedict(dict()), None)

    def test_collidedictall(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(8, 8, 10, 10)
        r4 = Rect(25, 25, 10, 10)
        rects = {"first": r1,
                 "second": r2,
                 "third": r3,
                 "fourth": r4}

        expected = [("first", r1), ("second", r2), ("third", r3)]

        result = r1.collidedictall(rects)
        for pair in expected:
            self.assertIn(pair, result)
        self.assertNotIn(("fourth", r4), result)

    def test_not_equal(self):
        r1 = Rect(0, 0, 0, 0)
        r2 = Rect(1, 1, 1, 1)
        r3 = Rect(0, 0, 0, 0)
        self.assertEqual(r1, r3)
        self.assertNotEqual(r1, r2)


class FRectTests(TestCase):

    def setUp(self):
        self.r = Rect(11.2, 12.3, 13.4, 14.5)

    def test_get_fx(self):
        self.assertEqual(self.r.fx, 11.2)

    def test_get_fy(self):
        self.assertEqual(self.r.fy, 12.3)

    def test_get_fright(self):
        self.assertEqual(self.r.fright, 24.6)

    def test_get_fbottom(self):
        self.assertEqual(self.r.fbottom, 26.8)

    def test_get_ftopleft(self):
        self.assertEqual((11.2, 12.3), self.r.ftopleft)

    def test_get_fbottomleft(self):
        self.assertEqual((11.2, 26.8), self.r.fbottomleft)

    def test_get_ftopright(self):
        self.assertEqual((24.6, 12.3), self.r.ftopright)

    def test_get_fbottomright(self):
        self.assertEqual((24.6, 26.8), self.r.fbottomright)

    def test_get_fcenterx(self):
        self.assertEqual(17.9, self.r.fcenterx)

    def test_get_fcentery(self):
        self.assertEqual(19.55, self.r.fcentery)

    def test_get_fcenter(self):
        self.assertEqual((17.9, 19.55), self.r.fcenter)

    def test_get_fmidtop(self):
        self.assertEqual((17.9, 12.3), self.r.fmidtop)

    def test_get_fmidleft(self):
        self.assertEqual((11.2, 19.55), self.r.fmidleft)

    def test_get_fmidbottom(self):
        self.assertEqual((17.9, 26.8), self.r.fmidbottom)

    def test_get_fmidright(self):
        self.assertEqual((24.6, 19.55), self.r.fmidright)

    def test_get_fsize(self):
        self.assertEqual((13.4, 14.5), self.r.fsize)

    def test_get_fwidth(self):
        self.assertEqual(13.4, self.r.fw)

    def test_get_fheight(self):
        self.assertEqual(14.5, self.r.fheight)

    def test_set_fx(self):
        self.r.fx = 12
        self.assertEqual(self.r.fx, 12)

    def test_set_fy(self):
        self.r.fy = 13
        self.assertEqual(self.r.fy, 13)

    def test_set_fright(self):
        self.r.fright = 28
        self.assertEqual(self.r.fright, 28)

    def test_set_fbottom(self):
        self.r.fbottom = 27
        self.assertEqual(self.r.fbottom, 27)

    def test_set_ftopleft(self):
        self.r.ftopleft = (13, 14)
        self.assertEqual((13, 14), self.r.ftopleft)

    def test_set_fbottomleft(self):
        self.r.fbottomleft = (12, 27)
        self.assertEqual((12, 27), self.r.fbottomleft)

    def test_set_ftopright(self):
        self.r.ftopright = (25, 13)
        self.assertEqual((25, 13), self.r.ftopright)

    def test_set_fbottomright(self):
        self.r.fbottomright = 25, 27
        self.assertEqual((25, 27), self.r.fbottomright)

    def test_set_fcenterx(self):
        self.r.fcenterx = 18
        self.assertEqual(18, self.r.fcenterx)

    def test_set_fcentery(self):
        self.r.fcentery = 20
        self.assertEqual(20, self.r.fcentery)

    def test_set_fcenter(self):
        self.r.fcenter = (18, 20)
        self.assertEqual((18, 20), self.r.fcenter)

    def test_fcenter_after_fscale(self):
        self.r = Rect(0, 0, 1, 1)
        center = self.r.fcenter
        new_center = self.r.fscale(2, 2).fcenter
        self.assertEqual((0.5, 0.5), center, new_center)

    def test_center_after_finflate(self):
        self.r = Rect(0.0, 0.0, 1.0, 1.0)
        center = self.r.fcenter
        new_center = self.r.finflate(2, 2).fcenter
        self.assertEqual((0.5, 0.5), center, new_center)

    def test_set_fmidtop(self):
        self.r.fmidtop = (18.0, 19.0)
        self.assertEqual((18, 19), self.r.fmidtop)

    def test_set_fmidleft(self):
        self.r.fmidleft = (12.0, 20.0)
        self.assertEqual((12, 20), self.r.fmidleft)

    def test_set_fmidbottom(self):
        self.r.fmidbottom = (18.0, 27.0)
        self.assertEqual((18, 27), self.r.fmidbottom)

    def test_set_fmidright(self):
        self.r.fmidright = (25.0, 20.0)
        self.assertEqual((25, 20), self.r.fmidright)

    def test_set_fsize(self):
        self.r.fsize = (14.0, 15.0)
        self.assertEqual((14, 15), self.r.fsize)

    def test_set_fw(self):
        self.r.fw = 14
        self.assertEqual(14, self.r.fw)

    def test_set_fh(self):
        self.r.fh = 15
        self.assertEqual(15, self.r.fh)

    def test_fcopy(self):
        r2 = self.r.fcopy()
        self.assertEqual(r2.ftopleft, self.r.ftopleft)
        self.assertEqual(r2.fsize, self.r.fsize)

    def test_fmove(self):
        x, y = self.r.ftopleft
        self.assertEqual((x + 9.8, y - 10), self.r.fmove(10, -10).ftopleft)

    def test_fmove_ip(self):
        x, y = self.r.ftopleft
        self.r.fmove_ip(10.0, -10.0)
        self.assertEqual((x + 10.0, y - 10.0), self.r.ftopleft)

    def test_fclamp_too_big(self):
        r1 = Rect(50.0, 50.0, 50.0, 50.0)
        r2 = Rect(0.0, 0.0, 100.0, 100.0)
        center = r2.fclamp(r1).fcenter
        self.assertEqual(r1.fcenter, center)

    def test_fclamp_from_above(self):
        r1 = Rect(0.0, 0.0, 25.0, 25.0)
        r2 = Rect(0.0, 100.0, 100.0, 100.0)
        r3 = r1.fclamp(r2)
        self.assertEqual(r3.ftopleft, (0, r2.ftop))

    def test_fclamp_from_below(self):
        # equal
        r1 = Rect(0.0, 200.0, 25.0, 25.0)
        r2 = Rect(0.0, 100.0, 100.0, 100.0)
        r3 = r1.fclamp(r2)
        self.assertEqual(r3.fbottomleft, (0, r2.fbottom))

        # greater
        r1 = Rect(0.0, 201.0, 25.0, 25.0)
        r2 = Rect(0.0, 100.0, 100.0, 100.0)
        r3 = r1.fclamp(r2)
        self.assertEqual(r3.fbottomleft, (0.0, r2.fbottom))

    # "clamp from the left, clamp from the right you're the only rect
    # in sight!" -- Jimmy Buffet

    def test_fclamp_from_the_left(self):
        r1 = Rect(0.0, 0.0, 25.0, 25.0)
        r2 = Rect(100.0, 0.0, 100.0, 100.0)
        r3 = r1.fclamp(r2)
        self.assertEqual(r3.ftopleft, (r2.fleft, 0.0))

    def test_fclamp_from_the_right(self):
        r1 = Rect(101.0, 0.0, 25.0, 25.0)
        r2 = Rect(0.0, 0.0, 100.0, 100.0)
        r3 = r1.fclamp(r2)
        self.assertEqual(r3.ftopright, (r2.fright, 0.0))

    def test_finflate(self):
        r = self.r.finflate(5, 5)
        self.assertEqual(r.fcenter, (17.5, 19.3))
        self.assertEqual(r.fsize, (self.r.fwidth + 4.6, self.r.fheight + 4.5))

    def test_fscale(self):
        r = self.r.fscale(2, 3)
        self.assertEqual(r.fcenter, (17.5, 19.3))
        self.assertEqual(r.fsize, (26, 42))

    def test_fclip(self):
        # bigger
        r1 = Rect(0, 0, 125, 125)
        r2 = Rect(25, 25, 100, 100)
        self.assertEqual(r1.fclip(r2).ftopleft, r2.ftopleft)
        self.assertEqual(r1.fclip(r2).fbottomright, r2.fbottomright)

        # smaller
        r1 = Rect(0, 0, 75, 75)
        r2 = Rect(25, 25, 100, 100)
        self.assertEqual(r1.fclip(r2).ftopleft, r2.ftopleft)
        self.assertEqual(r1.fclip(r2).fbottomright, r2.fsize)

    def test_funion(self):
        r1 = Rect(0, 0, 50, 50)
        r2 = Rect(25, 25, 50, 50)
        r3 = r1.funion(r2)
        self.assertEqual(r3.ftopleft, (0, 0))
        self.assertEqual(r3.fbottomright, (75, 75))

    def test_funionall(self):
        r1 = Rect(0, 0, 50, 50)
        r2 = Rect(25, 25, 50, 50)
        r3 = Rect(50, 50, 50, 50)
        r4 = r1.funionall([r1, r2, r3])
        self.assertEqual(r4.ftopleft, (0, 0))
        self.assertEqual(r4.fbottomright, (100, 100))

    def test_ffit_wider(self):
        r1 = Rect(0, 0, 50, 50)
        r2 = Rect(0, 0, 75, 20)
        r3 = r1.ffit(r2)
        self.assertEqual(r3.ftopleft, (27.5, 0))
        self.assertEqual(r3.fsize, (20, 20))

    def test_fnormalize(self):
        r1 = Rect(0, 0, -10, -10)
        r1.fnormalize()
        self.assertEqual(r1.ftopleft, (-10, -10))
        self.assertEqual(r1.fsize, (10, 10))

        r2 = Rect(0, 0, 10, 10)
        r2.fnormalize()
        self.assertEqual(r2.ftopleft, (0, 0))
        self.assertEqual(r2.fsize, (10, 10))

    def test_fcontains(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 3, 3)
        self.assertTrue(r1.fcontains(r2))
        self.assertFalse(r2.fcontains(r1))

    def test_fcollidepoint(self):
        r1 = Rect(0, 0, 15, 15)
        self.assertTrue(r1.fcollidepoint((10, 10)))
        self.assertFalse(r1.fcollidepoint((16, 10)))
        self.assertTrue(r1.fcollidepoint(10, 10))
        self.assertFalse(r1.fcollidepoint(16, 10))
        self.assertTrue(r1.fcollidepoint(10, 11, 12))

    def test_fcolliderect(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(20, 20, 10, 10)
        self.assertTrue(r1.fcolliderect(r2))
        self.assertTrue(r2.fcolliderect(r1))
        self.assertFalse(r1.fcolliderect(r3))
        self.assertFalse(r3.fcolliderect(r2))

    def test_fcollidelist(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(20, 20, 10, 10)
        r4 = Rect(25, 25, 10, 10)
        r5 = Rect(100, 100, 100, 100)
        rects = [r4, r3, r2]
        self.assertEqual(2, r1.fcollidelist(rects))
        self.assertEqual(-1, r5.fcollidelist(rects))

    def test_fcollidelistall(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(8, 8, 10, 10)
        r4 = Rect(25, 25, 10, 10)
        r5 = Rect(9, 9, 100, 100)
        rects = [r4, r3, r2, r5]
        self.assertEqual(r1.fcollidelistall(rects), [1, 2, 3])

    def test_fcollidedict(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(8, 8, 10, 10)
        r4 = Rect(25, 25, 10, 10)
        r5 = Rect(100, 100, 100, 100)
        rects = {"first": r1,
                 "second": r2,
                 "third": r3,
                 "fourth": r4}
        key, rect = r1.collidedict(rects)
        self.assertIn(key, rects)
        self.assertIn(rect, rects.values())
        self.assertNotEqual(id(rect), id(r1))
        self.assertEqual(r5.fcollidedict(rects), None)
        self.assertEqual(r1.fcollidedict(dict()), None)

    def test_fcollidedictall(self):
        r1 = Rect(0, 0, 10, 10)
        r2 = Rect(5, 5, 10, 10)
        r3 = Rect(8, 8, 10, 10)
        r4 = Rect(25, 25, 10, 10)
        rects = {"first": r1,
                 "second": r2,
                 "third": r3,
                 "fourth": r4}

        expected = [("first", r1), ("second", r2), ("third", r3)]

        result = r1.fcollidedictall(rects)
        for pair in expected:
            self.assertIn(pair, result)
        self.assertNotIn(("fourth", r4), result)
