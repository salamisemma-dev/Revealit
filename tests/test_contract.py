import json
import hashlib
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

    def test_homepage_visual_adjustments_are_kept_in_sync(self):
        root = Path(__file__).parents[1]
        html = (root / 'index.html').read_text(encoding='utf-8')
        header = (root / 'components/reveal.tsx').read_text(encoding='utf-8')
        home = (root / 'app/page.tsx').read_text(encoding='utf-8')
        styles = (root / 'app/globals.css').read_text(encoding='utf-8')
        layout = (root / 'app/layout.tsx').read_text(encoding='utf-8')
        workflow = (root / '.github/workflows/pages.yml').read_text(encoding='utf-8')
        package = json.loads((root / 'package.json').read_text(encoding='utf-8'))

        self.assertNotIn('Over Reveal It', html)
        self.assertNotIn('Over Reveal It', header)
        self.assertNotIn('urvinbanda.chatgpt.site', html)
        self.assertNotIn('urvinbanda.chatgpt.site', layout)
        self.assertIn('Onze aanpak', html)
        self.assertIn('Onze aanpak', header)
        self.assertNotIn('next/link', header)
        for href in ['href="/reveal-fit/"', 'href="/foundation/"', 'href="/contact/"', 'href="/foundation/anbi/"', 'href="/privacy/"']:
            self.assertIn(href, header)
        for href in ['href="reveal-fit/"', 'href="foundation/"', 'href="contact/"']:
            self.assertIn(href, html)

        self.assertNotIn('class="word"', html)
        self.assertNotIn('world-word', home)
        self.assertNotIn('world-word', styles)
        self.assertFalse((root / 'public/images/fit-foundation-watermark.svg').exists())
        self.assertIn('border-radius:999px', html)
        self.assertIn('border-radius:999px', styles)
        self.assertIn('position:absolute', html)
        self.assertIn('position:absolute', styles)
        self.assertIn('top:-.075em', html)
        self.assertIn('top:-.075em', styles)
        self.assertIn('wordmark-it">it<span className="wordmark-period"', header)
        self.assertIn('border:1px solid var(--sand)', html)
        self.assertIn('border:1px solid #cbb68f', styles)

        watermark = 'public/images/reveal-transition-silhouettes.png'
        self.assertTrue((root / watermark).is_file(), watermark)
        self.assertIn(watermark, html)
        self.assertIn('/images/reveal-transition-silhouettes.png', styles)
        self.assertEqual(hashlib.sha256((root / watermark).read_bytes()).hexdigest(), '0099d0f4d25e9ececdb61d57f07a4b19cc0a649fbcf3d09db75449792dec3b5b')
        self.assertIn('background-size:280% auto', html)
        self.assertIn('background-size:280% auto', styles)
        self.assertIn('background-size:330% auto', html)
        self.assertIn('background-size:330% auto', styles)
        self.assertIn('-webkit-mask-image:linear-gradient(90deg,#000 0 56%,transparent 82%)', styles)
        self.assertIn('-webkit-mask-image:linear-gradient(90deg,transparent 0 18%,#000 46%)', styles)
        self.assertIn('background:linear-gradient(135deg,#2f2821,#4a3a2b)', styles)
        self.assertIn('background:linear-gradient(135deg,#d9cdbb,#eee6da)', styles)
        self.assertIn('node scripts/export-pages.mjs', workflow)
        self.assertIn('PAGES_BASE_PATH: /Revealit', workflow)
        self.assertIn('--ignore-pattern "pages-dist/**"', package['scripts']['lint'])
