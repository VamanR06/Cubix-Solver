''''
             |------------|
             |-U1--U2--U3-|
             |------------|
             |-U4--U5--U6-|
             |------------|
             |-U7--U8--U9-|
|------------|------------|------------|------------|
|-L1--L2--L3-|-F1--F2--F3-|-R1--R2--R3-|-B1--B2--B3-|
|------------|------------|------------|------------|
|-L4--L5--L6-|-F4--F5--F6-|-R4--R5--R6-|-B4--B5--B6-|
|------------|------------|------------|------------|
|-L7--L8--L9-|-F7--F8--F9-|-R7--R8--R9-|-B7--B8--B9-|
|------------|------------|------------|------------|
             |-D1--D2--D3-|
             |------------|
             |-D4--D5--D6-|
             |------------|
             |-D7--D8--D9-|
             |------------|

             
U - Orange
L - White
F - Green
R - Yellow
B - Blue
D - Red

Map each face color to the corresponding ULFRBD value

U R F D L B - Order to type pieces out for a scramble string
'''

__all__ = ["Cube", "Face", "Piece"]

from typing import Dict, List
from dataclasses import dataclass
from itertools import batched
from kociemba import solve

colors_to_faces = {
    "orange": "U",
    "yellow": "L",
    "green": "F",
    "white": "R",
    "blue": "B",
    "red": "D"
}

@dataclass
class Piece:
    face: "Face"
    color: str
    position: int

    def __repr__(self):
        return self.color[0].capitalize()

class Face:
    def __init__(self, side: str, pieces: List[str]):
        if len(pieces) != 9:
            raise ValueError("Face must have 9 pieces")
        
        self.side = side
        self.pieces = [Piece(face=self, color=color, position=pos) for pos, color in enumerate(pieces)]

    def __repr__(self):
        return "Face: " + self.side + "\n" + "\n".join([' '.join([str(piece) for piece in row]) for row in batched(self.pieces, 3)])

class Cube:
    FACE_ORDER = ["U", "R", "F", "D", "L", "B"]
    def __init__(self, faces: Dict[str, List[str]] = None):
        self.faces = {side: Face(side=side, pieces=faces[side]) if faces else None for side in self.FACE_ORDER}

    def set_face(self, side: str, pieces: List[str]):
        self.faces[colors_to_faces[side]] = Face(side=colors_to_faces[side], pieces=pieces)

    def solve(self):
        if not all(face.pieces for face in self.faces.values()):
            raise ValueError("Cube must have all faces")

        cube_string = ""
        for face in self.FACE_ORDER:
            for piece in self.faces[face].pieces:
                cube_string += colors_to_faces[piece.color.lower()]

        return solve(cube_string)

    def print(self):
        for i in self.faces:
            print(self.faces[i])

    def __repr__(self):
        return "\n".join([str(face) for face in self.faces])