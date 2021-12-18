FLAVORS = {
    "Mint": "./drawings/flavor-mint.svg",
    "Strawberry": "./drawings/flavor-strawberry.svg",
    "Bubble Gum": "./drawings/flavor-bubblegum.svg",
    "Banana": "./drawings/flavor-banana.svg",
}
WRAPPERS = {
    "None": "none",
    "Checkers": "./drawings/wrapper-checkers.svg",
    "Dots": "./drawings/wrapper-dots.svg",
    "Hearts": "./drawings/wrapper-hearts.svg",
    "Stripes": "./drawings/wrapper-stripes.svg",
}


def get_lines(image):
    with open(image, "r") as f:
        lines = f.readlines()
    return lines


def get_flavor(flavor):
    return get_lines(FLAVORS[flavor])


def get_wrapper(wrapper):
    wrapper = WRAPPERS[wrapper]
    if wrapper == "none":
        return []
    return get_lines(wrapper)


def get_color(color):
    lines = get_lines("drawings/gum-color.svg")
    return [line.replace('fill="#000000"', f'fill="#{color}"') for line in lines]


def get_base():
    return get_lines("drawings/gum-base.svg")


def save_gum(path, lines):
    with open(path, "w") as f:
        f.write(
            '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" shape-rendering="crispEdges" viewBox="0 1 58 54">\n'
        )
        f.writelines(lines)
        f.write(
            "</svg>",
        )


def create_image(path, flavor, wrapper, color):
    lines = []

    lines.extend(get_color(color))
    lines.extend(get_wrapper(wrapper))
    lines.extend(get_flavor(flavor))
    lines.extend(get_base())

    save_gum(path, lines)
