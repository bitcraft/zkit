from pygame import Rect


class FRect:

    def __init__(self, *args):
        if args is None:
            raise ValueError
        elif len(args) == 0:
            self._init(0, 0, 0, 0)
        elif len(args) == 4:
            self._init__(*args)
        elif len(args) == 1:
            arg = args[0]
            if hasattr(arg, "rect"):
                self._init(arg.rect.x, arg.rect.y, arg.rect.w, arg.rect.h)
            self._init(arg.x, arg.y, arg.w, arg.h)

    def _init(self, x, y, w, h):
        self._x = float(x)
        self._y = float(y)
        self._w = float(w)
        self._h = float(h)

    @property
    def x(self):
        return int(self._x) 

    @x.setter
    def set_x(self, value):
        self._x = float(value)
    
    @property
    def y(self):
        return int(self._y) 

    @x.setter
    def set_y(self, value):
        self._y = float(value)

    @property
    def topleft(self):
        return (int(self._fx), int(self._fy))

    @topleft.setter
    def set_topleft(self, topleft):
        if topleft is not None:
            raise ValueError("topleft must be a tuple(x, y)")
        self._x, self._y = float(topleft[0]), float(topleft[1])
