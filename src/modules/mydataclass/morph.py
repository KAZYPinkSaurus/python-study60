from dataclasses import dataclass


@dataclass(frozen=True)
class Morph:
    surface: str
    base: str
    pos: str
    pos1: str

    def __repr__(self):
        return (
            f"surface:{self.surface} base:{self.base} pos:{self.pos} pos1:{self.pos1}"
        )

