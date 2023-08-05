# Licensed under a 3-clause BSD style license - see LICENSE.rst
from numpy.testing import assert_allclose
import pytest
from astropy.coordinates import SkyCoord
import astropy.units as u
from regions import CircleSkyRegion
from ...data import DataStore, Observations, ObservationStats, SpectrumStats
from ...utils.testing import requires_data
from ...background import ReflectedRegionsBackgroundEstimator


@pytest.fixture(scope="session")
def observations():
    data_store = DataStore.from_dir("$GAMMAPY_DATA/hess-dl3-dr1/")
    run_list = [23523, 23526]
    return Observations([data_store.obs(_) for _ in run_list])


@pytest.fixture(scope="session")
def on_region():
    pos = SkyCoord(83.63 * u.deg, 22.01 * u.deg)
    on_size = 0.3 * u.deg
    return CircleSkyRegion(pos, on_size)


@pytest.fixture(scope="session")
def bad_on_region():
    pos = SkyCoord(83.6333 * u.deg, 21.5144 * u.deg)
    on_size = 0.3 * u.deg
    return CircleSkyRegion(pos, on_size)


@pytest.fixture(scope="session")
def stats(on_region, observations):
    obs = observations[0]
    bge = ReflectedRegionsBackgroundEstimator(on_region=on_region, observations=obs)
    bg = bge.process(obs)
    return ObservationStats.from_observation(obs, bg)


@pytest.fixture(scope="session")
def stats_bad_on_region(bad_on_region, observations):
    obs = observations[0]
    bge = ReflectedRegionsBackgroundEstimator(on_region=bad_on_region, observations=obs)
    bg = bge.process(obs)
    return ObservationStats.from_observation(obs, bg)


@pytest.fixture(scope="session")
def stats_stacked(on_region, observations):
    bge = ReflectedRegionsBackgroundEstimator(
        on_region=on_region, observations=observations
    )
    bge.run()

    return ObservationStats.stack(
        [
            ObservationStats.from_observation(obs, bg)
            for obs, bg in zip(observations, bge.result)
        ]
    )


@pytest.fixture(scope="session")
def stats_stacked_bad_on_region(bad_on_region, observations):
    bge = ReflectedRegionsBackgroundEstimator(
        on_region=bad_on_region, observations=observations
    )
    bge.run()

    return ObservationStats.stack(
        [
            ObservationStats.from_observation(obs, bg)
            for obs, bg in zip(observations, bge.result)
        ]
    )


@requires_data()
class TestObservationStats:
    @staticmethod
    def test_str(stats):
        text = str(stats)
        assert "Observation summary report" in text

    @staticmethod
    def test_to_dict(stats):
        data = stats.to_dict()
        assert data["n_on"] == 425
        assert data["n_off"] == 395
        assert_allclose(data["alpha"], 0.333, rtol=1e-2)
        assert_allclose(data["sigma"], 16.430, rtol=1e-3)
        assert_allclose(data["gamma_rate"].value, 11.127, rtol=1e-3)
        assert_allclose(data["bg_rate"].value, 4.995, rtol=1e-3)
        assert_allclose(data["livetime"].value, 26.362, rtol=1e-3)

    @staticmethod
    def test_bad_on(stats_bad_on_region):
        data = stats_bad_on_region.to_dict()
        assert data["alpha"] == 0

    @staticmethod
    def test_stack(stats_stacked):
        data = stats_stacked.to_dict()
        assert data["n_on"] == 900
        assert data["n_off"] == 766
        assert_allclose(data["alpha"], 0.333, rtol=1e-2)
        assert_allclose(data["sigma"], 25.244, rtol=1e-3)

    @staticmethod
    def test_stack_bad_on(stats_stacked_bad_on_region):
        data = stats_stacked_bad_on_region.to_dict()
        assert data["n_on"] == 156
        assert data["n_off"] == 1006
        assert_allclose(data["alpha"], 0.125, rtol=1e-3)
        assert_allclose(data["livetime"].value, 26.211, rtol=1e-3)


@pytest.fixture(scope="session")
def spectrum_stats(on_region, observations):
    obs = observations[0]
    bge = ReflectedRegionsBackgroundEstimator(on_region=on_region, observations=obs)
    bg = bge.process(obs)
    e_range = [1 * u.TeV, 10 * u.TeV]
    return SpectrumStats.from_observation_in_range(obs, bg, e_range)


@requires_data("gammapy-data")
class TestSpectrumStats:
    @staticmethod
    def test_str(spectrum_stats):
        text = str(spectrum_stats)
        assert "Observation summary report" in text
        assert "energy range" in text

    @staticmethod
    def test_to_dict(spectrum_stats):
        data = spectrum_stats.to_dict()
        assert data["energy_min"] == 1 * u.TeV
        assert data["energy_max"] == 10 * u.TeV
