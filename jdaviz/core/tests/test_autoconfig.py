# Tests automatic config detection against our example notebook data

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from astroquery.mast import Observations

from jdaviz import open as jdaviz_open
from jdaviz.configs import Specviz, Specviz2d, Cubeviz, Imviz


@pytest.mark.remote_data
@pytest.mark.filterwarnings('ignore')
@pytest.mark.parametrize('uris', (
    ("mast:JWST/product/jw02732-o004_t004_miri_ch1-shortmediumlong_x1d.fits", Specviz),
    ("mast:JWST/product/jw01538-o160_s00004_nirspec_f170lp-g235h-s1600a1-sub2048_s2d.fits", Specviz2d),  # noqa
    ("mast:JWST/product/jw02727-o002_t062_nircam_clear-f090w_i2d.fits", Imviz),
    ("mast:JWST/product/jw02732-o004_t004_miri_ch1-shortmediumlong_s3d.fits", Cubeviz))
)
def test_autoconfig(uris):
    # Setup temporary directory
    with TemporaryDirectory(ignore_cleanup_errors=True) as tempdir:
        uri = uris[0]
        helper_class = uris[1]
        download_path = str(Path(tempdir) / Path(uri).name)
        Observations.download_file(uri, local_path=download_path)

        viz_helper = jdaviz_open(download_path, show=False)

        assert type(viz_helper) == helper_class
        assert len(viz_helper.app.data_collection) > 0
