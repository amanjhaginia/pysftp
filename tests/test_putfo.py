'''test pysftp.Connection.putfo - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *
from io import BytesIO
from mock import Mock, call


@skip_if_ci
def test_putfo_callback_fsize(lsftp):
    '''test putfo with callback and file_size'''
    rfile = 'a-test-file'
    buf = b'I will not buy this record, it is scratched\nMy hovercraft'\
          b' is full of eels.'
    fsize = len(buf)
    bwrote = fsize
    flo = BytesIO(buf)
    cback = Mock(return_value=None)
    lsftp.putfo(flo, rfile, file_size=fsize, callback=cback)
    lsftp.remove(rfile)
    assert cback.call_count >= 2
    # we didn't specify file size, so second arg is 0
    assert cback.call_args_list == [call(bwrote, fsize), call(bwrote, fsize)]


@skip_if_ci
def test_putfo_callback(lsftp):
    '''test putfo with callback'''
    rfile = 'a-test-file'
    buf = b'I will not buy this record, it is scratched\nMy hovercraft'\
          b' is full of eels.'
    flo = BytesIO(buf)
    cback = Mock(return_value=None)
    lsftp.putfo(flo, rfile, callback=cback)
    lsftp.remove(rfile)
    assert cback.call_count >= 2
    # we didn't specify file size, so second arg is 0
    assert cback.call_args_list == [call(len(buf), 0), call(len(buf), 0)]


@skip_if_ci
def test_putfo_flo(lsftp):
    '''test putfo in simple form'''
    rfile = 'a-test-file'
    buf = b'I will not buy this record, it is scratched\nMy hovercraft'\
          b' is full of eels.'
    flo = BytesIO(buf)
    assert rfile not in lsftp.listdir()
    rslt = lsftp.putfo(flo, rfile)
    assert rfile in lsftp.listdir()
    lsftp.remove(rfile)
    assert rslt.st_size == len(buf)


@skip_if_ci
def test_putfo_no_remotepath(lsftp):
    '''test putfo raises TypeError when not specifying a remotepath'''
    buf = b'I will not buy this record, it is scratched\nMy hovercraft'\
          b' is full of eels.'
    flo = BytesIO(buf)
    with pytest.raises(TypeError):
        lsftp.putfo(flo)


def test_putfo_ro_srv(psftp):
    '''test error returned from attempting to putfo to a read-only server'''
    buf = b'I will not buy this record, it is scratched\nMy hovercraft'\
          b' is full of eels.'
    flo = BytesIO(buf)
    with pytest.raises(TypeError):
        psftp.putfo(flo)
