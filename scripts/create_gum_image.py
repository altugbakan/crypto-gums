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


def get_lines(path: str) -> list[str]:
    with open(path, "r") as f:
        lines = [line for line in f.readlines() if "svg" not in line]
    return lines


def get_flavor(flavor: str) -> list[str]:
    return get_lines(FLAVORS[flavor])


def get_wrapper(wrapper: str) -> list[str]:
    wrapper = WRAPPERS[wrapper]
    if wrapper == "none":
        return []
    return get_lines(wrapper)


def get_color(color: str) -> list[str]:
    lines = get_lines("drawings/gum-color.svg")
    return [line.replace('fill="#000000"', f'fill="#{color}"') for line in lines]


def get_base() -> list[str]:
    return get_lines("drawings/gum-base.svg")


def save_gum(path: str, lines: list[str]):
    with open(path, "w") as f:
        f.writelines(lines)


def create_image(flavor: str, wrapper: str, color: str, path: str = None) -> list[str]:
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" shape-rendering="crispEdges" viewBox="0 1 58 54">\n',
        *get_color(color),
        *get_wrapper(wrapper),
        *get_flavor(flavor),
        *get_base(),
        "</svg>",
    ]

    if path:
        save_gum(path, lines)

    return lines
