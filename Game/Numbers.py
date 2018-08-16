
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Number display

from Engine.Entity import *
from Engine.Vector import *
import Engine.Storage

class Numbers:
    def __init__(self, number: int, pos: Vector3, color: Vector4 = Vector4(1,1,1,1), total_digits: int=6, size: float=8):
        self._texture: Texture = Engine.Storage.get(Engine.Storage.Type.TEXTURE, 'numbers')
        self.position: Vector3 = pos
        self.color = color
        self.size: float = size
        self.number: int = number
        self.total_digits: int = total_digits

    def update_number(self, number):
        self.number = number

    def draw(self):
        self._texture.bind()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBegin(GL_QUADS)
        glColor(self.color.x, self.color.y, self.color.z, self.color.w)

        _numbers: List[int] = []

        for i in range(self.total_digits):
            # Add correct digit
            _numbers.append(math.floor(self.number % pow(10, i+1) / pow(10, i+0)))
        # Reverse
        _numbers = list(reversed(_numbers))

        for i in range(len(_numbers)):
            _num: int = _numbers[i]
            # Bottom Left
            glTexCoord2f(_num/10, 0)
            glVertex2f(
                self.position.x + (self.size * i),
                self.position.y
            )

            # Bottom Right
            glTexCoord2f(_num/10 + 1/10, 0)
            glVertex2f(
                self.position.x + self.size + (self.size * i),
                self.position.y
            )

            # Top Right
            glTexCoord2f(_num/10 + 1/10, 1)
            glVertex2f(
                self.position.x + self.size + (self.size * i),
                self.position.y + self.size
            )

            # Top Left
            glTexCoord2f(_num/10, 1)
            glVertex2f(
                self.position.x + (self.size * i),
                self.position.y + self.size
            )

        glEnd()
