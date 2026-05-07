from src.claim_normalizer import ClaimNormalizer
from tests.claim_test_data import VALID_CLAIM_RECORD


class TestNormalizer:
    def setup_method(self):
        self._normalizer = ClaimNormalizer()

    def test_normalize_valid_claim(self):
        print("Start test_normalize_valid_claim")
        # given
        record = VALID_CLAIM_RECORD

        # when
        result = self._normalizer.normalize(record)

        # then
        assert result is not None
