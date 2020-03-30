import st4


def test_st4():
    s = st4.ST4('/dev/ttyUSB0')
    s.go_rapid(0, 0)
    assert s.readline() == 'Rapid to:,X0,Y0,Z0,W0'
