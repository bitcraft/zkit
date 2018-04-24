"""
   Pygame uses FRect objects to store and manipulate rectangular areas. A FRect
   can be created from a combination of left, top, width, and height values.
   FRects can also be created from python objects that are already a FRect or
   have an attribute named "rect".

   Any Pygame function that requires a FRect argument also accepts any of these
   values to construct a FRect. This makes it easier to create FRects on the fly
   as arguments to functions.

   The FRect functions that change the position or size of a FRect return a new
   copy of the FRect with the affected changes. The original FRect is not
   modified. Some methods have an alternate "in-place" version that returns
   None but effects the original FRect. These "in-place" methods are denoted
   with the "ip" suffix.

   The FRect object has several virtual attributes which can be used to move and
   align the FRect:

   ::

       x,y
       top, left, bottom, right
       topleft, bottomleft, topright, bottomright
       midtop, midleft, midbottom, midright
       center, centerx, centery
       size, width, height
       w,h

   All of these attributes can be assigned to:

   ::

       rect1.right = 10
       rect2.center = (20,30)

   Assigning to size, width or height changes the dimensions of the rectangle;
   all other assignments move the rectangle without resizing it. Notice that
   some attributes are integers and others are pairs of integers.

   If a FRect has a nonzero width or height, it will return True for a nonzero
   test. Some methods return a FRect with 0 size to represent an invalid
   rectangle.

   The coordinates for FRect objects are all integers. The size values can be
   programmed to have negative values, but these are considered illegal FRects
   for most operations.

   There are several collision tests between other rectangles. Most python
   containers can be searched for collisions against a single FRect.

   The area covered by a FRect does not include the right- and bottom-most edge
   of pixels. If one FRect's bottom border is another FRect's top border (i.e.,
   rect1.bottom=rect2.top), the two meet exactly on the screen but do not
   overlap, and ``rect1.colliderect(rect2)`` returns false.

   Though FRect can be subclassed, methods that return new rectangles are not
   subclass aware. That is, move or copy return a new :mod:`pygame.FRect`
   instance, not an instance of the subclass. This may change. To make subclass
   awareness work though, subclasses may have to maintain the same constructor
   signature as FRect.
"""

class FRect:

    def __init__(self, *args):
        """
        FRect(left, top, width, height) -> FRect
        FRect((left, top), (width, height)) -> FRect
        FRect(object) -> FRect
        """
        if len(args) == 4:
            # left, top, width, height
            self._init(*args)
        elif len(args) == 2:
            # (left, top), (width, height)
            self._init(args[0][0], args[0][1], args[1][0], args[1][1])
        elif len(args) == 1:
            rect = args[0]
            self._init(rect.left, rect.top, rect.width, rect.height)
        else:
            raise ValueError("Invalid arguments passed to FRect initializer")

    def _init(self, left, top, width, height):
        self._left = float(left)
        self._top = float(top)
        self._width = float(width)
        self._height = float(height)

    def __len__(self):
        return 4

    def __getitem__(self, index):
        if index == 0:
            return self.left
        elif index == 1:
            return self.top
        elif index == 2:
            return self.width
        elif index == 3:
            return self.height
        else:
            # TODO: fix this.
            # a rect object must support slicing, but python throws
            # an exception with using the the modulo operator on a slice.
            # this is just a hack...for now!
            # return self[index]      # max recursion error
            # return self[index % 4]  # type error
            return [self.left, self.top, self.width, self.height][index]

    def __iter__(self):
        yield self.left
        yield self.top
        yield self.width
        yield self.height

    def __repr__(self):
        return "pygame2.FRect(left=%.2f, top=%.2f, width=%.2f, height=%.2f)" % \
               (self.left, self.top, self.width, self.height)

    def __eq__(self, other):
        return list(self) == list(other)

    def __ne__(self, other):
        return not list(self) == list(other)

    @property
    def left(self):
        return int(self._left)
    
    @left.setter
    def left(self, value):
        self._left = float(value)
    
    @property
    def top(self):
        return int(self._top)

    @top.setter
    def top(self, value):
        self._top = float(value)

    @property
    def width(self):
        return int(self._width)

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return int(self._height)

    @height.setter
    def height(self, value):
        self._height = float(value)

    @property
    def x(self):
        """
        Returns the left edge of the rect
        """
        return self.left

    @x.setter
    def x(self, value):
        self.left = value

    @property
    def y(self):
        """
        Returns the top edge of the rect
        """
        return self.top

    @y.setter
    def y(self, value):
        self.top = value

    @property
    def right(self):
        """
        Returns the x value which is the right edge of the rect
        """
        return self.left + self.width

    @right.setter
    def right(self, value):
        self.left = value - self.width

    @property
    def bottom(self):
        """
        Returns the y value of the bottom edge of the rect
        """
        return self.top + self.height

    @bottom.setter
    def bottom(self, value):
        self.top = value - self.height

    @property
    def topleft(self):
        """
        Returns a point (x, y) which is the top, left corner of the rect.
        """
        return (self.left, self.top)

    @topleft.setter
    def topleft(self, value):
        self.left, self.top = value

    @property
    def bottomleft(self):
        """
        Returns a point (x, y) which is the bottom, left corner of the rect.
        """
        return (self.left, self.bottom)

    @bottomleft.setter
    def bottomleft(self, value):
        self.left, self.bottom = value

    @property
    def topright(self):
        """
        Returns a point (x, y) which is the top, right corner of the rect.
        """
        return (self.right, self.top)

    @topright.setter
    def topright(self, value):
        self.right, self.top = value

    @property
    def bottomright(self):
        """
        Returns a point (x, y) which is the bottom, right corner of the rect.
        """
        return (self.right, self.bottom)

    @bottomright.setter
    def bottomright(self, value):
        self.right, self.bottom = value

    @property
    def centerx(self):
        """
        Returns the center x value of the rect
        """
        return self.left + self.width // 2

    @centerx.setter
    def centerx(self, value):
        self.left = value - self.width // 2

    @property
    def centery(self):
        """
        Returns the center y value of the rect
        """
        return self.top + self.height // 2

    @centery.setter
    def centery(self, value):
        self.top = value - self.height // 2

    @property
    def center(self):
        """
        Returns a point (x, y) which is the center of the rect.
        """
        return (self.centerx, self.centery)

    @center.setter
    def center(self, value):
        self.centerx, self.centery = value

    @property
    def midtop(self):
        """
        Returns a point (x, y) which is the midpoint of the top edge
        the rect.
        """
        return (self.centerx, self.top)

    @midtop.setter
    def midtop(self, value):
        self.centerx, self.top = value

    @property
    def midleft(self):
        """
        Returns a point (x, y) which is the midpoint of the left edge
        the rect.
        """
        return (self.left, self.centery)

    @midleft.setter
    def midleft(self, value):
        self.left, self.centery = value

    @property
    def midbottom(self):
        """
        Returns a point (x, y) which is the midpoint of the bottom edge
        the rect.
        """
        return (self.centerx, self.bottom)

    @midbottom.setter
    def midbottom(self, value):
        self.centerx, self.bottom = value

    @property
    def midright(self):
        """
        Returns a point (x, y) which is the midpoint of the right edge of
        the rect.
        """
        return (self.right, self.centery)

    @midright.setter
    def midright(self, value):
        self.right, self.centery = value

    @property
    def size(self):
        """
        Returns the width and height of the rect as a tuple (width, height)
        """
        return (self.width, self.height)

    @size.setter
    def size(self, value):
        self.width, self.height = value

    @property
    def w(self):
        """
        The width of the rect
        """
        return self.width

    @w.setter
    def w(self, value):
        self.width = value

    @property
    def h(self):
        """
        The height of the rect
        """
        return self.height

    @h.setter
    def h(self, value):
        self.height = value

    def scale(self, x, y):
        """
        Returns a new rectangle with size changed by given scaling factor. The
        rectangle remains centered around its current center. Negative values
        will shrink the rectangle.
        """
        return FRect(self).scale_ip(x, y)

    def scale_ip(self, x, y):
        """
        Same as ``FRect.scale()``, but mutates the instance
        """
        center = self.center
        self.width *= x
        self.height *= y
        self.center = center
        return self

    def copy(self):
        """
        Returns a new rectangle having the same position and size as
        the original.
        """
        return FRect(self)

    def move(self, offset_or_x, y=None):
        """
        Returns a new rectangle that is moved by the given offset. The x
        and y arguments can be any integer value, positive or negative.
        """
        if y is None:
            offset_or_x, y = offset_or_x
        return FRect(self).move_ip(offset_or_x, y)

    def move_ip(self, x, y):
        """
        Same as ``FRect.move()``, but mutates the instance
        """
        self.left += x
        self.top += y
        return self

    def inflate(self, x, y):
        """
        Returns a new rectangle with the size changed by the given offset. The
        rectangle remains centered around its current center. Negative values
        will shrink the rectangle.
        """
        return FRect(self).inflate_ip(x, y)

    def inflate_ip(self, x, y):
        """
        Same as ``FRect.inflate()``, but mutates the instance
        """
        center = self.center
        self.width += x
        self.height += y
        self.center = center
        return self

    def clamp(self, other_rect):
        """
        Move the rect the least amount of distance necessary to place it
        inside of other_rect. If other_rect is smaller in height,
        width or both then the rect shall be centered on those
        dimensions which do not fit.
        """
        return FRect(self).clamp_ip(other_rect)

    def clamp_ip(self, other_rect):
        """
        Same as ``FRect.clamp()``, but mutates the instance
        """
        if other_rect.width <= self.width:
            self.centerx = other_rect.centerx
        elif other_rect.left > self.left:
            self.left = other_rect.left
        elif other_rect.right < self.left:
            self.left = other_rect.right - self.width

        if other_rect.height <= self.height:
            self.centery = other_rect.centery
        elif other_rect.top >= self.bottom:
            self.top = other_rect.top
        elif other_rect.bottom <= self.top:
            self.bottom = other_rect.bottom

        return self

    def clip(self, other_rect):
        """
        Returns a new rectangle that is cropped to be completely inside
        the argument FRect. If the two rectangles do not overlap to
        begin with, a FRect with 0 size is returned.
        """
        r = FRect(max(other_rect.left, self.left),
                 max(other_rect.top, self.top),
                 self.width, self.height)

        if r.right > other_rect.right:
            r.width -= r.right - other_rect.right
        if r.bottom > other_rect.bottom:
            r.height -= r.bottom - other_rect.bottom

        return r

    def union(self, other_rect):
        """
        Returns a new rectangle that completely covers the area of the two
        provided rectangles. There may be area inside the new FRect that is not
        covered by the originals.
        """
        return FRect(self).union_ip(other_rect)

    def union_ip(self, other_rect):
        """
        Same as ``FRect.union()``, but mutates the instance
        """
        self.left = min(other_rect.left, self.left)
        self.top = min(other_rect.top, self.top)
        right = max(self.right, other_rect.right)
        bottom = max(self.bottom, other_rect.bottom)
        self.width = right - self.left
        self.height = bottom - self.top
        return self

    def unionall(self, other_rects):
        """
        Returns the union of one rectangle with a sequence of many rectangles.
        """
        result = FRect(self)
        result.unionall_ip(other_rects)
        return result

    def unionall_ip(self, other_rects):
        """
        The same as the ``FRect.unionall()`` method, but mutates the rect
        instance.
        """
        for rect in other_rects:
            self.union_ip(rect)
        return self

    def fit(self, other_rect):
        """
        Returns a new rectangle that is moved and resized to fit
        another. The aspect ratio of the original FRect is preserved,
        so the new rectangle may be smaller than the target in either
        width or height.
        """
        x_ratio = float(self.width) / float(other_rect.width)
        y_ratio = float(self.height) / float(other_rect.height)
        max_ratio = max(x_ratio, y_ratio)
        width = self.width / max_ratio
        height = self.height / max_ratio
        left = other_rect.left + (other_rect.width - width) / 2
        top = other_rect.top + (other_rect.height - height) / 2
        return FRect(left, top, width, height)

    def normalize(self):
        """
        This will flip the width or height of a rectangle if it has a
        negative size. The rectangle will remain in the same place,
        with only the sides swapped.
        """
        if self.width < 0:
            self.left += self.width
            self.width = abs(self.width)

        if self.height < 0:
            self.top += self.height
            self.height = abs(self.height)

    def contains(self, other_rect):
        """
        Returns true when the argument is completely inside the FRect.
        """
        return self.top <= other_rect.top \
               and self.left <= other_rect.left \
               and self.right >= other_rect.right \
               and self.bottom >= other_rect.bottom

    def collidepoint(self, *args):
        """
        Returns true if the given point is inside the rectangle. A point along
        the right or bottom edge is not considered to be inside the rectangle.
        """
        if len(args) == 1:
            # (x, y)
            x, y = args[0]
        else:
            # x, y, ...
            x, y = args[0:2]
        return x >= self.left \
               and y >= self.top \
               and x <= self.right \
               and y <= self.bottom

    def colliderect(self, other_rect):
        """
        Returns true if any portion of either rectangle overlap (except the
        top+bottom or left+right edges).
        """
        return self.left < other_rect.right \
               and self.top < other_rect.bottom \
               and self.right > other_rect.left \
               and self.bottom > other_rect.top

    def collidelist(self, other_rects):
        """
        Test whether the rectangle collides with any in a sequence of
        rectangles.  The index of the first collision found is
        returned. If no collisions are found an index of -1 is
        returned.
        """
        for i, rect in enumerate(other_rects):
            if self.colliderect(rect):
                return i
        return -1

    def collidelistall(self, other_rects):
        """
        Returns a list of all the indices that contain rectangles that
        collide with the FRect. If no intersecting rectangles are
        found, an empty list is returned.
        """
        indices = []
        for i, rect in enumerate(other_rects):
            if self.colliderect(rect):
                indices.append(i)
        return indices

    def collidedict(self, other_rects):
        """
        Returns the key and value of the first dictionary value that collides
        with the FRect. If no collisions are found, None is returned.

        FRect objects are not hashable and cannot be used as keys in a
        dictionary, only as values.
        """
        for key, value in other_rects.items():
            if id(self) != id(value):
                if self.colliderect(value):
                    return key, value

    def collidedictall(self, other_rects):
        """
        Returns a list of all the key and value pairs that intersect with
        the FRect. If no collisions are found an empty dictionary is
        returned.

        FRect objects are not hashable and cannot be used as keys in a
        dictionary, only as values.
        """
        pairs = list()
        for key, value in other_rects.items():
            if self.colliderect(value):
                pairs.append((key, value))
        return pairs

