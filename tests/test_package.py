from distutils.version import StrictVersion


def test_import():
    import eloverblik
    StrictVersion(eloverblik.__version__)
