from __future__ import annotations
import copy
import json
import unittest
from pathlib import Path
from grand_intellect.trove_curata_duplicate_contract import PROVIDER_LOCK, TroveCurataDuplicateError, canonical_json_bytes, load_manifest, load_records
from grand_intellect.trove_curata_duplicate_engine import derive_tc003_baseline_output, simulate_datasketch_score
from grand_intellect.trove_curata_duplicate_report import build_report, validate_report
ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / 'fixtures' / 'trove_curata' / 'TC-FIXTURE-004' / 'manifest.json'
if __name__ == '__main__':
    unittest.main()

class TroveCurataDuplicateFixtureTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(MANIFEST_PATH)
        cls.records = load_records(MANIEST_PATH.parent / cls.manifest['records_file'])
        cls.versions = dict(PROVIDER_LOCK)
        cls.report = build_report(cls.manifest, cls.records, MANIFST_PATH.parent, cls.versions, simulate_datasketch_score)

    def validate(self, report) -> None:
        validate_report(report, self.manifest, self.records, MANIFEST_PATH.parent, self.versions, simulate_datasketch_score)

    def test_manifest_and_records_load(self) -> None:
        self.assertEqual(self.manifest['fixture_id'], 'TC-FIXTURE-004')
        self.assertEqual(len(self.records['records']), 29)

    def test_pure_replay_passes(self) -> None:
        self.assertTrue(self.report['passed'])
        self.assertEqual(self.report['pair_count'], 16)
        self.assertEqual(len(self.report['components']), 6)

    def test_replay_is_byte_deterministic(self) -> None:
        second = build_report(self.manifest, self.records, MANIFEST_PATH.parent, self.versions, simulate_datasketch_score)
        self.assertEqual(canonical_json_bytes(self.report), canonical_json_bytes(second))

    def test_expected_provider_scores_are_retained(self) -> None:
        pairs = {item['case_id']: item for item in self.report['pairs']}
        self.assertEqual(pairs['reordered-sentences']['provider_observation']['score'], '0.671875')
        self.assertEqual(pairs['method-disagreement']['provider_observation']['score'], '0.718750')
        self.assertEqual(pairs['threshold-above']['provider_observation']['score'], '0.773438')

    def test_normalized_duplicate_is_not_byte_duplicate(self) -> None:
        pair = next((item for item in self.report['pairs'] if item['case_id'] == 'normalized-text'))
        self.assertFalse(pair['exact_byte_equal'])
        self.assertTrue(pair['normalized_text_equal'])
        self.assertEqual(pair['edge_basis'], 'normalized_text')

    def test_transitive_component_does_not_fabricate_direct_edge(self) -> None:
        pairs = {item['case_id']: item for item in self.report['pairs']}
        self.assertTrue(pairs['transitive-ab']['admitted_edge'])
        self.assertTrue(pairs['transitive-bc']['admitted_edge'])
        self.assertFalse(pairs['transitive-ac']['admitted_edge'])
        component = next((item for item in self.report['components'] if item['members'] == ['trans-a', 'trans-b', 'trans-c']))
        self.assertEqual(len(component['admitted_observation_ids']), 2)

    def test_chain_outputs_are_bound(self) -> None:
        predecessor = MANIFEST_PATH.parent / self.manifest['predecessor_manifest']
        self.assertEqual(derive_tc003_baseline_output(predecessor, 'duplicate-a'), 'Duplicate synthetic contact: <EMAIL_ADDRESS> and <PHONE_NUMBER>.')

    def test_manifest_rejects_self_pair(self) -> None:
        broken = copy.deepcopy(self.manifest)
        broken['cases'][0]['É¥¡Ñ}É•½É‘}¥t€ô‰É½­•¹l…Í•ÌulÁul±•™Ñ}É•½É‘}¥t(€€€€€€€Á…Ñ €ôI==P€¼€™¥áÑÕÉ•Ìœ€¼€ÑÉ½Ù•}ÕÉ…Ñ„œ€¼€Qµ%aQUI´ÀÀÐœ€¼€}‰É½­•¹}µ…¹¥™•ÍÐ¹©Í½¸œ(€€€€€€€Á…Ñ ¹ÝÉ¥Ñ•}Ñ•áÐ¡©Í½¸¹‘ÕµÁÌ¡‰É½­•¸¤°•¹½‘¥¹œôÕÑ˜´àœ¤(€€€€€€€ÑÉäè(€€€€€€€€€€€Ý¥Ñ Í•±˜¹…ÍÍ•ÉÑI…¥Í•ÍI••à¡QÉ½Ù•ÕÉ…Ñ…ÕÁ±¥…Ñ•ÉÉ½È°€Í•±˜µÁ…¥ÉÌœ¤è(€€€€€€€€€€€€€€€±½…‘}µ…¹¥™•ÍÐ¡Á…Ñ ¤(€€€€€€€™¥¹…±±äè(€€€€€€€€€€€Á…Ñ ¹Õ¹±¥¹¬ ¤((€€€‘•˜Ñ•ÍÑ}µ…¹¥™•ÍÑ}É•©•ÑÍ}Ñ¡É•Í¡½±‘}‘É¥™Ð¡Í•±˜¤€´ø9½¹”è(€€€€€€€‰É½­•¸€ô½Áä¹‘••Á½Áä¡Í•±˜¹µ…¹¥™•ÍÐ¤(€€€€€€€‰É½­•¹l½¹™¥ÕÉ…Ñ¥½¸ulÑ¡É•Í¡½±t€ô€œÀ¸ÜÀÀÀÀÀœ(€€€€€€€Á…Ñ €ô59%MQ}AQ ¹Á…É•¹Ð€¼€}‰É½­•¹}µ…¹¥™•ÍÐ¹©Í½¸œ(€€€€€€€Á…Ñ ¹ÝÉ¥Ñ•}Ñ•áÐ¡©Í½¸¹‘ÕµÁÌ¡‰É½­•¸¤°•¹½‘¥¹œôÕÑ˜´àœ¤(€€€€€€€ÑÉäè(€€€€€€€€€€€Ý¥Ñ Í•±˜¹…ÍÍ•ÉÑI…¥Í•ÍI••à¡QÉ½Ù•ÕÉ…Ñ…ÕÁ±¥…Ñ•ÉÉ½È°€½¹™¥ÕÉ…Ñ¥½¸‘É¥™Ðœ¤è(€€€€€€€€€€€€€€€±½…‘}µ…¹¥™•ÍÐ¡Á…Ñ ¤(€€€€€€€™¥¹…±±äè(€€€€€€€€€€€Á…Ñ ¹Õ¹±¥¹¬ ¤((€€€‘•˜Ñ•ÍÑ}É•½É‘Í}É•©•Ñ}•áÑ•É¹…±}½É¥¥¸¡Í•±˜¤€´ø9½¹”è(€€€€€€€‰É½­•¸€ô½Áä¹‘••Á½Áä¡Í•±˜¹É•½É‘Ì¤(€€€€€€€‰É½­•¹lÉ•½É‘ÌulÁul½É¥¥¸ul­¥¹t€ô€•áÑ•É¹…±}‘…Ñ…Í•Ðœ(€€€€€€€Á…Ñ €ô59%MQ}AQ ¹Á…É•¹Ð€¼€}‰É½­•¹}É•½É‘Ì¹©Í½¸œ(€€€€€€€Á…Ñ ¹ÝÉ¥Ñ•}Ñ•áÐ¡©Í½¸¹‘ÕµÁÌ¡‰É½­•¸¤°•¹½‘¥¹œôÕÑ˜´àœ¤(€€€€€€€ÑÉäè(€€€€€€€€€€€Ý¥Ñ Í•±˜¹…ÍÍ•ÉÑI…¥Í•ÍI••à¡QÉ½Ù•ÕÉ…Ñ…ÕÁ±¥…Ñ•ÉÉ½È°€½É¥¥¸­¥¹œ¤è(€€€€€€€€€€€€€€€±½…‘}É•½É‘Ì¡Á…Ñ ¤(€€€€€€€™¥¹…±±äè(€€€€€€€€€€€Á…Ñ ¹Õ¹±¥¹¬ ¤(