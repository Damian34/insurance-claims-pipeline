from src.claim_analyzer import ClaimAnalyzer
from src.claim_normalizer import ClaimNormalizer
from tests.claim_test_data import VALID_CLAIM_RECORD, INVALID_CLAIM_RECORD


class TestAnalyzer:
    def setup_method(self):
        self._normalizer = ClaimNormalizer()
        self._analyzer = ClaimAnalyzer()

    def test_analyze_valid_claim(self):
        print("Start test_analyze_valid_claim")
        # given
        record = self._normalizer.normalize(VALID_CLAIM_RECORD)

        # when
        result = self._analyzer.calculate_and_enrich(record)

        # then
        assert result["is_approved"] is True
        assert result["payout_amount"] > 0
        assert result["rejection_reasons"] == []

    def test_analyze_invalid_claim(self):
        print("Start test_analyze_invalid_claim")
        # given
        record = self._normalizer.normalize(INVALID_CLAIM_RECORD)

        # when
        result = self._analyzer.calculate_and_enrich(record)

        # then
        assert result["is_approved"] is False
        assert result["payout_amount"] == 0.0
        assert len(result["rejection_reasons"]) > 0