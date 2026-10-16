# east73studio.com

The website for East 73 Studio LLC. It's plain HTML and CSS: no framework, no build step, no tracking.

```
/                      index.html                  Home
/expressed/            expressed/index.html        Expressed product page
/expressed/privacy/    expressed/privacy/index.html
/expressed/terms/      expressed/terms/index.html
/expressed/support/    expressed/support/index.html
(any missing page)     404.html
css/site.css           The only stylesheet. Colors and fonts are at the top, in :root
js/site.js             Footer year and image fade-in. That's all
images/                Logos, app icon, Open Graph images
fonts/                 Self-hosted Newsreader, Inter, Saira (OFL)
tools/make_images.py   Regenerates favicons and OG images (rarely needed)
```

To publish the site for the first time, follow **[DEPLOY.md](DEPLOY.md)**.

---

## Preview the site on your computer

From the repo folder, run:

```bash
python -m http.server 8000
```

Then open http://localhost:8000. Press Ctrl+C in the terminal to stop it.

(Opening the HTML files directly by double-clicking them won't look right, because the pages use paths like `/css/site.css` that need a server.)

## Updating the site later

Every change follows the same four steps:

1. **Edit** the file (for example, `index.html`).
2. **Check** it with the local preview above.
3. **Commit**, which saves a snapshot with a note:
   ```bash
   git add -A
   ```
   ```bash
   git commit -m "Add Spotted Amazon link"
   ```
4. **Push**, which uploads it. GitHub Pages republishes the site automatically within a minute or two:
   ```bash
   git push
   ```

---

## Asset checklist

Until you add the real images, the site shows gray placeholder blocks. To find every placeholder in the code, search the project for `{{` or `TO BE WRITTEN`.

### Images

- [x] **Expressed app icon.** Already in place (`images/expressed/app-icon-256.webp` / `-512.webp`), converted from the app repo's 1024px icon.
- [ ] **Expressed screenshots.** Done: Can Make, AI discovery, Pantry, and My Bottles (home card). Still needed: **Bottle scan** (`screen-bottle-scan.webp`), shot with an unbranded bottle. Save as WebP in `images/expressed/`, for example `screen-can-make.webp`, `screen-bottle-scan.webp`, `screen-discovery.webp`, `screen-pantry.webp`. Use straight screenshots with no device frame (the site draws the phone). Around 600px wide is plenty.
  - `expressed/index.html`: each `<div class="screen placeholder">Screenshot</div>` has a comment above it with the exact `<img>` line to swap in.
  - `index.html`: the Expressed card has one more screenshot placeholder.
- [ ] **Spotted cover.** In `index.html`, replace the `<div class="card-media placeholder ratio-book" …>` block with `<img class="card-media fade" src="/images/spotted-cover.webp" alt="Cover of Spotted: A Field Guide to the Fifty States" loading="lazy">`. Any 4:3 image works, such as the cover on a plain background.
- [x] **3 state posters.** Done: Colorado, Utah, New Mexico in `images/posters/` (Wyoming saved there as a spare). Same idea: replace the `posters-fan` block with one 4:3 image of three posters (for example `images/posters.webp`).

To convert a PNG or JPG to WebP, export as WebP from Preview or Photoshop, or use https://squoosh.app (it runs in your browser and nothing is uploaded).

### Links and text

| Placeholder | Where | What to do |
|---|---|---|
| ~~`{{SPOTTED_URL}}`~~ | `index.html` | ✅ Done: https://www.amazon.com/dp/B0HHXNTZB6 |
| ~~`{{POSTERS_URL}}`~~ | `index.html` | ✅ Done: https://www.etsy.com/shop/East73Studio |
| `{{CONTACT_EMAIL}}` | footer of every page, Support, Privacy, Terms | Currently `hello@east73studio.com`. **Create that alias in iCloud before launch** (see below). To use a different address, find-and-replace across all files |
| `{{ABOUT_TEXT}}` | `index.html`, About section | The brief's draft is in place. Approve or edit it |
| Home headline | `index.html`, `<h1>` | "Small, carefully made things." is a suggestion. Change it freely |
| `{{DATE}}`, `[TO BE WRITTEN]` | Privacy, Terms | Paste in the real text when it's drafted. The app repo's `PRIVACY_POLICY.md` is a starting point |
| FAQ | Support | Replace the three `[Question …]` placeholders |

### At App Store launch

- [ ] `expressed/index.html`, line near the top: change `<body data-app-store="soon">` to `data-app-store="live"`.
- [ ] In the same file, replace `href="#"` on the `appstore-live` link with `{{APP_STORE_URL}}`, your App Store link.
- [ ] Download Apple's black **"Download on the App Store"** badge (SVG) from https://developer.apple.com/app-store/marketing/guidelines/ and save it as `images/expressed/app-store-badge.svg`.
- [ ] Uncomment the `apple-itunes-app` meta tag in the `<head>` and put in `{{APP_STORE_ID}}` (the number after `id` in your App Store URL).

---

## Things to do outside this repo

1. **Create the email alias.** On iPhone: Settings → your name → iCloud → iCloud Mail → Custom Email Domain → east73studio.com → add `hello@east73studio.com`. (Or at icloud.com → Account Settings → Custom Email Domain.)
2. **Redirect expressed.app.** In Namecheap, for **expressed.app**: Advanced DNS → add a **URL Redirect Record** for host `@` and one for `www`, both pointing to `https://east73studio.com/expressed/`, type **Permanent (301)**. Leave **Mail Settings** on **Email Forwarding**, so `hello@expressed.app` keeps working.
3. **Update App Store Connect** once the site is live (App Information and the version page):
   - Privacy Policy URL: `https://east73studio.com/expressed/privacy/`
   - Support URL: `https://east73studio.com/expressed/support/`
   - Marketing URL: `https://east73studio.com/expressed/`

   Apple checks that the privacy policy page has real content, so publish the actual policy before you submit the app for review.

---

## Design notes

- **Colors and fonts.** All of them live in `:root` at the top of `css/site.css`. The Expressed colors (`#141414`, `#EF9F27`) are the exact values from the app's `tailwind.config.js`.
- **Fonts are self-hosted** rather than loaded from Google Fonts, so visitors' browsers never contact a third party. That keeps the privacy story to "no third parties, no cookies."
- **Logo files** come from the East 73 logo generator (`C:\Users\sstoo\OneDrive\East 73 Studio LLC\Logo`). If the logo changes, copy the new SVGs into `images/brand/` and rerun `tools/make_images.py`. That script needs `pip install pillow resvg-py`.
