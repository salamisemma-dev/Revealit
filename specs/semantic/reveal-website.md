---
id: semantic-reveal-website
type: semantic
version: 1.8.0
status: approved
owner: Reveal It user brief
---

## Intent
Translate the user-authorized PDF into a premium Dutch website with distinct Fit and Foundation journeys.

## Contract
Routes /, /reveal-fit, /foundation, /foundation/anbi, /contact, /privacy. The published offering follows lib/site-content.json. Contact prepares a message locally; it must never imply transmission. No live checkout or donation collection before business details are supplied.

## Business rules
Offer all nine specified services. Two brand routes remain first-screen choices. Never invent proof, ANBI registration, contacts, prices or partners. Forms cannot solicit health data. Use generated photos only as illustrative scenes.

## Homepage hero motion
The homepage opens with the supplied 10-second cinematic video as a layered, sticky story. The video is used only in the hero. Desktop and mobile receive separate optimized encodes and immediate posters; the inactive encode must not be started. Playback starts only while the hero is visible. Scroll controls spatial layers and narrative emphasis rather than repeatedly seeking the compressed video. Navigation, copy and calls to action remain usable without motion. `prefers-reduced-motion` keeps the poster static. Decorative depth layers remain hidden from assistive technology.

## Homepage structure
The homepage stays visually clean and uses the existing cream, dark-brown, sand and gold identity. After the hero, content is limited to the core philosophy, a decisive Fit/Foundation split, the three-step approach and one closing action. Reveal Fit and the Foundation must look and read as distinct destinations without inventing outcomes, partners, prices, projects or registration status.

## Mobile and editorial slides
The discovery cue in the cinematic hero uses a restrained gold glow. Reveal Fit and Foundation each use a manually controlled editorial slider with large touch targets, arrow-key support and swipe gestures. Sliders do not autoplay. Each photographic asset is used once across the published pages; supporting slides use typography and brand surfaces instead of repeating imagery. Small screens keep controls visible, copy readable and layouts free of horizontal overflow.

The homepage hero keeps Reveal Fit and Foundation together as two calm, clearly separated choices on every viewport. The Reveal Fit button is one solid brown surface with a restrained gold sheen passing over it, without a gold border or enclosing capsule. Foundation uses a muted sand-brown surface for contrast. Both destinations remain visible within the sticky frame. The redundant centred discovery cue is omitted. Decorative numbered progress tracks are omitted from both the hero and the editorial sliders; sliders retain only explicit previous and next buttons. A source watermark or provenance mark in supplied media is not removed or obscured; replacing it requires a clean user-supplied export.

## Downstream impact
Controls page content, navigation, message topics, asset use and the later launch checklist. Live booking/payments require an explicit contract update and supplied merchant details.

## Static homepage export
The repository root contains a standalone `index.html` companion for GitHub Pages. It preserves the homepage brand, responsive cinematic hero, reduced-motion behavior and primary Fit/Foundation journeys without requiring the application runtime. It references tracked `public/` media and sends secondary-route actions to the canonical live Site.

## Verification
Readiness contract data checks: tests/test_contract.py::test_offering_and_routes, tests/test_contract.py::test_no_fabricated_operational_data. Runtime verification after implementation: browser navigation, mobile menu, message validation/preview/download, one h1, images, console and overflow; evidence recorded in delivery.md.

Hero verification: production build succeeds; the interactive layer has a non-JavaScript visual baseline, uses `prefers-reduced-motion`, and does not make pointer movement a prerequisite for any action.

Message behavior: tests/message.test.mjs verifies valid draft and invalid inputs. Optional WebMCP prepare_reveal_message uses the same validation and visible draft state, with sent:false.
