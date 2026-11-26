# Carousel Design Brief

Nov 14, 2026 · @Gooseberry

Build one reusable Instagram carousel system (Canva or Figma) for a sales-tips page aimed at sales heads and sales managers across industries, with the goal of becoming the page they trust. Every post is a 7–10 slide carousel, 4–5 per week, so speed of reuse matters more than one-off polish.

## Brand basics

The page must look like an independent sales-education brand, not a software company.

| Item | Direction |
| --- | --- |
| Page name | \[To be decided\] — short, sales-flavoured, works as a handle |
| Audience | Sales heads, VPs of sales and sales managers who run teams — B2B and B2C, every channel (calls, email, LinkedIn, WhatsApp, field), India first |
| Personality | Trusted, practical, calm authority — an experienced sales leader sharing what works, not a guru or a corporate brand |
| Tone of visuals | Clean, premium, framework- and data-friendly, text-led, mobile-first |
| Feel to avoid | SaaS product marketing, hustle-guru hype, stock-photo corporate, meme clutter |

- Do not reuse PyngDesk or Wabadesk colours, fonts, logo shapes or illustration style anywhere in this system.
- Logo: a simple wordmark of the page name plus a square avatar version for the profile picture (readable at 110 px).
- Reference style: text-first educational carousel pages such as Owlnomics — for structure and clarity only, not to copy their look.

## Colour palette

One dark base, one light base, one accent and two signal colours; every slide uses at most three of them. Values below are a starting proposal — the designer may adjust, but keep the roles and contrast.

| Role | Proposed hex | Use |
| --- | --- | --- |
| Ink (dark base) | #111418 | Hook and CTA backgrounds, body text on light slides |
| Paper (light base) | #F6F4EF | Value-slide backgrounds |
| Accent | #FFC21A | Highlighted words, numbers, swipe arrow — never large blocks of body text |
| Good / do | #1FA855 | "Say this" boxes, ticks |
| Bad / don't | #E5484D | "Don't say this" boxes, crosses |
| Muted | #8A8F98 | Slide numbers, handle tag, captions |

- Text contrast must pass WCAG AA (4.5:1) against its background.
- Accent appears on 1–3 words per slide, so it stays the thing the eye lands on.

## Typography

Two free Google fonts: a heavy sans for headlines and a readable sans for body, so the system works in both Canva and Figma.

| Style | Font (proposal) | Size at 1080 px wide | Max words |
| --- | --- | --- | --- |
| Hook headline (slide 1) | Inter Tight or Archivo, Black/ExtraBold | 96–120 px | 10 |
| Slide headline | Same, Bold | 64–76 px | 8 |
| Body | Inter, Medium | 40–44 px | 30 |
| Script / quote line | Inter, SemiBold Italic | 40 px | 25 |
| Small label (slide no., handle) | Inter, Medium | 26–28 px | 4 |

- Line height 1.1 for headlines, 1.35 for body; left-aligned, never justified.
- Maximum 30 words on any slide, including headline; if more is needed, split into two slides.
- Sentence case everywhere; ALL CAPS only for one- or two-word labels like "SAY THIS".
- Must stay readable at phone size — test every template by viewing it at 375 px wide.

## Canvas and grid

Every slide is 1080 × 1350 px (4:5 portrait), exported as PNG.

| Element | Spec |
| --- | --- |
| Outer margin | 80 px left/right, 96 px top/bottom |
| Grid | 6 columns, 24 px gutters inside the margins |
| Profile-grid safe zone | Key words of slide 1 inside the centre 1080 × 1080 area (the profile grid crops to about 3:4) |
| Slide number | Top-right, muted, format "2/9" |
| Handle tag | Bottom-left on every slide, muted, small — survives screenshots and reshares |
| Swipe cue | Bottom-right arrow on every slide except the last |

- Keep the same positions for slide number, handle and swipe cue across all templates so a carousel reads as one piece.
- Alternate dark and light backgrounds only by template rule (next section), not at random.

## Slide templates

Design these seven templates; every carousel is assembled from them by swapping text only.

| # | Template | Background | Layout | Used as |
| --- | --- | --- | --- | --- |
| T1 | Hook | Ink | Huge headline, 1–2 accent words, small "Swipe →" cue | Slide 1 |
| T2 | Second hook | Ink or Paper | Short headline + one stat or pain line | Slide 2 (Instagram often re-shows carousels from slide 2) |
| T3 | Tip | Paper | Number badge, headline, 1–2 lines of body | Value slides |
| T4 | Do this / Don't do this | Paper | Red box above, green box below, one line each | Scripts, coaching, management mistakes |
| T5 | Conversation | Paper | Mock of an email, LinkedIn DM, WhatsApp chat or call script, 2–5 lines + one caption | Scripts, objections, 1:1 coaching talks |
| T6 | Cheat sheet | Ink | Numbered recap list of the whole carousel, 5–8 lines | Second-last slide (the one people save) |
| T7 | CTA | Ink | One action (Save / Share / Comment a keyword), avatar, handle | Last slide |
| T9 | Framework | Paper | Simple diagram: funnel, 2×2, steps or pyramid, with short labels | Pipeline stages, hiring scorecards, coaching models |
| T10 | Metric | Ink or Paper | One big number or a simple bar/line chart + one-line takeaway | Benchmarks, KPIs, forecasting, team performance |

- A standard carousel runs T1 → T2 → T3/T4/T5 × 4–6 → T6 → T7.
- T7 needs three variants: "Save this", "Share with your team", and "Comment \[KEYWORD\] for the free PDF".
- T8 (Tool card) is specified in the next-but-one section. Also design a profile-grid cover variant of T1 so the feed looks consistent.

## Components

Build these as reusable components so each new carousel takes minutes, not hours.

| Component | Spec |
| --- | --- |
| Conversation mocks | Four generic styles — email, LinkedIn-style DM, WhatsApp-style chat, call-script card; fictional names and avatars only; no real platform logos or Meta/LinkedIn branding; editable text throughout |
| Framework shapes | Funnel, 2×2 matrix, numbered steps, pyramid, before/after split — in the palette, with editable labels |
| Chart styles | Bar, line and big-number styles in the palette, no gridline clutter, one highlighted value in Accent |
| Number badge | Accent circle or square with 1–99, for tip slides |
| Do / Don't boxes | Rounded boxes in Good and Bad colours with a tick or cross icon |
| Highlight | Accent underline or marker behind 1–3 words |
| Swipe arrow | Small, consistent, bottom-right |
| Handle tag | @handle in muted small text, bottom-left |
| Icon set | One line-icon style (e.g. Lucide or Phosphor), 2 px stroke, about 20 icons: phone, email, chat, calendar, clock, money, target, team, person, funnel, pipeline, chart, trophy, handshake, check, cross, warning, star, gift, link |
| Lead-magnet mockup | A PDF-cover mockup for "Comment \[KEYWORD\]" CTA slides |

- No stock photos of people in suits; if a person appears, use flat illustration in one consistent style.
- Conversation mocks must use made-up names, companies and numbers only.

## Tool and disclosure slide

Add one extra template, T8 Tool card, for "tools for sales teams" posts; every tool, including PyngDesk, uses the same card so the post stays fair and consistent.

| Element | Spec |
| --- | --- |
| Layout | Tool name, its logo (with permission or plain text), one-line "best for", 2–3 strengths |
| Equal treatment | Same size, colours and position for every tool; PyngDesk gets no bigger card or special colour |
| Disclosure label | On the PyngDesk card itself: a clear tag such as "Built by our team" or "Our product", 32 px minimum, high contrast, inside the main content area — never in small print or the margin |
| Caption rule | Disclosure also goes in the first line of the caption (writer's job; noted here so the designer leaves no doubt on-slide) |

- The disclosure tag must be visible without zooming on a phone (ASCI expects disclosure to be prominent and upfront).
- Keep the tag wording editable so the team can adjust it.

## Deliverables and handoff

Deliver one editable template file plus the brand assets, ready for the content team to produce carousels without the designer.

- [ ] Logo wordmark + square profile avatar (SVG and PNG)
- [ ] Colour styles and text styles set up in the file
- [ ] Templates T1–T10 as editable pages or frames, plus the three T7 CTA variants
- [ ] Component library: conversation mocks, framework shapes, chart styles, badges, boxes, highlight, arrow, handle tag, icons, PDF mockup
- [ ] Two fully built sample carousels (one team-management framework post, one objection-handling post) as proof the system works
- [ ] Export preset: PNG, 1080 × 1350, sRGB
- [ ] One-page usage guide: which template for which slide, word limits, do/don't

| Item | Detail |
| --- | --- |
| Tool | Canva (preferred for speed) or Figma — \[team to confirm\] |
| File naming | YYYY-MM-DD\_topic-slug\_slideNN.png |
| Open questions | Final page name and handle; Canva vs Figma; whether a second page later reuses this system with a different accent colour |
