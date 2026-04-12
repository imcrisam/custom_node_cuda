try:
    from VHS.utils import strip_path
    HAS_VHS = True
except ImportError:
    HAS_VHS = False
    strip_path = lambda x: x


def path_widget(extensions: list = []):
    widget = {"placeholder": "output/my_file.pt"}
    if HAS_VHS:
        widget["vhs_path_extensions"] = extensions
    return widget