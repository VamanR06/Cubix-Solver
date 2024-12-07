from solver import Cube

solved = {
    "Up": ["orange", "orange", "orange", "orange", "orange", "orange", "orange", "orange", "orange"],
    "Down": ["red", "red", "red", "red", "red", "red", "red", "red", "red"],
    "Front": ["green", "green", "green", "green", "green", "green", "green", "green", "green"],
    "Right": ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
    "Back": ["blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue"],
    "Left": ["yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow"]
}

u_state = {
    "Up": ["orange", "orange", "orange", "orange", "orange", "orange", "orange", "orange", "orange"],
    "Down": ["red", "red", "red", "red", "red", "red", "red", "red", "red"],
    "Front": ["yellow", "yellow", "yellow", "green", "green", "green", "green", "green", "green"],
    "Right": ["green", "green", "green", "white", "white", "white", "white", "white", "white"],
    "Back": ["white", "white", "white", "blue", "blue", "blue", "blue", "blue", "blue"],
    "Left": ["blue", "blue", "blue", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow"]
}

u_r_state = {
    "Up": ["blue", "blue", "blue", "orange", "orange", "orange", "orange", "orange", "orange"],
    "Down": ["red", "red", "green", "red", "red", "green", "red", "red", "green"],
    "Front": ["yellow", "yellow", "yellow", "green", "green", "orange", "green", "green", "orange"],
    "Right": ["green", "green", "orange", "white", "white", "white", "white", "white", "white"],
    "Back": ["white", "white", "white", "red", "blue", "blue", "red", "blue", "blue"],
    "Left": ["red", "blue", "blue", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow"]
}

random_state = {
    "Up": ["green", "yellow", "orange", "green", "orange", "white", "yellow", "blue", "yellow"],
    "Down": ["white", "white", "white", "orange", "red", "red", "blue", "blue", "red"],
    "Front": ["blue", "white", "blue", "blue", "green", "green", "orange", "orange", "orange"],
    "Right": ["red", "green", "yellow", "orange", "white", "green", "blue", "white", "yellow"],
    "Back": ["green", "red", "red", "red", "blue", "blue", "green", "red", "red"],
    "Left": ["white", "yellow", "orange", "orange", "yellow", "yellow", "white", "yellow", "green"]
}

cube = Cube(random_state)
print(cube.solve())