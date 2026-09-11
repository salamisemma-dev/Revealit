import json
import unittest
from pathlib import Path

class WebsiteContract(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((Path(__file__).parents[1] / 'lib/site-content.json').read_text())

    def test_offering_and_routes(self):
        self.assertEqual(len(self.data['services']), 9)
        self.assertEqual(len(set(self.data['services'])), 9)
        self.assertEqual(set(self.data['routes']), {'/', '/reveal-fit', '/foundation', '/foundation/anbi', '/contact', '/privacy'})

    def test_no_fabricated_operational_data(self):
        for field in ['recipient', 'paymentUrl', 'rsin', 'kvk']:
            self.assertIsNone(self.data[field])
        self.assertEqual(self.data['contactMode'], 'local-draft')

    def test_standalone_index_video_sources_are_lazy_and_tracked(self):
        root = Path(__file__).parents[1]
        html = (root / 'index.html').read_text(encoding='utf-8')
        self.assertIn('data-public-src="public/media/hero-cinematic-desktop.mp4"', html)
        self.assertIn('data-public-src="public/media/hero-cinematic-mobile.mp4"', html)
        self.assertIn('data-root-src="/media/hero-cinematic-desktop.mp4"', html)
        self.assertIn('data-root-src="/media/hero-cinematic-mobile.mp4"', html)
        self.assertNotIn('autoplay', html.lower())
        for asset in [
            'public/media/hero-cinematic-desktop.mp4',
            'public/media/hero-cinematic-mobile.mp4',
            'public/media/hero-poster-desktop.webp',
            'public/media/hero-poster-mobile.webp',
        ]:
            self.assertTrue((root / asset).is_file(), asset)
