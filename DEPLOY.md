# Deploying east73studio.com

## Where to host it: GitHub Pages

I recommend **GitHub Pages**. Cloudflare Pages and Netlify are both good, but GitHub Pages fits this site best:

- **Your iCloud email is safest with it.** Pages only needs a few records **added** at your current DNS provider. Cloudflare Pages wants you to move the whole domain's DNS to Cloudflare, which means copying the iCloud mail records over by hand, and one typo breaks email.
- **One account, not two.** The code is on GitHub anyway, and Pages is a setting on that same repo.
- **Free, with automatic HTTPS.** It serves `/404.html`, and `/expressed/` maps to `expressed/index.html` with no setup.
- **The trade-off: the repo must be public** on the free plan. That's fine here. There are no secrets in it, only the website itself. Your commit name and email (`Scott <hello@east73studio.com>`) will also be public, which is fine since hello@ is already the public contact address.

---

## Step 1: Put the repo on GitHub

1. Sign in at github.com. Click **+** (top right), then **New repository**.
2. Name it `east73studio-site`. Set it to **Public**. Do **not** tick "Add a README" (you already have one). Click **Create repository**.
3. GitHub shows a page with a URL like `https://github.com/YOUR-USERNAME/east73studio-site.git`. In a terminal, run these two commands. The first tells your local repo where GitHub is; the second uploads your commits.

   ```bash
   git -C C:/Users/sstoo/east73studio-site remote add origin https://github.com/YOUR-USERNAME/east73studio-site.git
   ```
   ```bash
   git -C C:/Users/sstoo/east73studio-site push -u origin main
   ```
   The first push opens a browser window to sign in to GitHub. That's normal.

## Step 2: Turn on GitHub Pages

1. In the repo on GitHub, go to **Settings → Pages**.
2. Under **Build and deployment**, set Source to **Deploy from a branch**, Branch to **main**, folder **/ (root)**. Click **Save**.
3. After about a minute the site is live at `https://YOUR-USERNAME.github.io/east73studio-site/`. Some styles and links will look broken at that address because the site expects to live at the root of a domain. That fixes itself once the custom domain is set.
4. Still in Settings → Pages, type `east73studio.com` under **Custom domain** and click **Save**. (The repo's `CNAME` file already says this; the box just confirms it.)

**Recommended:** verify the domain so nobody else can claim it on GitHub. Go to your **profile picture → Settings → Pages → Add a domain**, enter `east73studio.com`, and GitHub gives you one TXT record to add (step 3 below). It's an *extra* TXT record and doesn't touch your email records.

## Step 3: Point the domain at GitHub (DNS)

> ### ⚠️ Read this first: protect your iCloud email
> Your domain receives email through **iCloud+ custom email domain**. That depends on DNS records that are already set up. **Do not change or delete any of them:**
>
> | Type | Host | Looks like | Leave alone |
> |---|---|---|---|
> | MX | `@` | `mx01.mail.icloud.com` and `mx02.mail.icloud.com` | ✅ keep |
> | TXT | `@` | `v=spf1 include:icloud.com ~all` | ✅ keep |
> | TXT | `@` | `apple-domain=…` | ✅ keep |
> | CNAME | `sig1._domainkey` | `sig1.dkim.east73studio.com.at.icloudmailadmin.com` | ✅ keep |
>
> **Before you change anything, screenshot the whole DNS page.** If email ever stops working, that screenshot is how you put it back.
>
> If your DNS is at **Namecheap**: leave **Mail Settings** (lower on the Advanced DNS page) set to **Custom MX**. Switching it to anything else silently deletes your iCloud MX records.

Go to your domain's DNS settings. At Namecheap that's **Domain List → Manage → Advanced DNS**.

**Remove only these, if they exist** (Namecheap adds them as a "parking page" by default; they aren't email records):
- a **URL Redirect Record** for host `@`
- a **CNAME** for host `www` pointing to `parkingpage.namecheap.com`

**Add these records:**

| Type | Host | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `YOUR-USERNAME.github.io.` |
| TXT | *(from GitHub's domain verification)* | *(value GitHub gave you)* |

Optional, for IPv6 visitors: four AAAA records on `@` with the values `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.

These records only control where web browsers go. Email uses the MX records, which you didn't touch.

DNS changes usually take effect within 30 minutes, but can take up to a day.

**Check email still works:** send a message to hello@east73studio.com from another account, and reply to it.

## Step 4: Make sure HTTPS works

1. Back in **Settings → Pages**, wait until it says *"Your site is live at https://east73studio.com"* and the DNS check shows a green tick. GitHub then issues a free HTTPS certificate automatically. This can take up to an hour after DNS updates.
2. Tick **Enforce HTTPS**. (If it's greyed out, the certificate isn't ready yet. Come back later.)
3. Test these three addresses. All should end up at `https://east73studio.com/` with the padlock showing:
   - `http://east73studio.com`
   - `https://www.east73studio.com`
   - `https://east73studio.com/expressed/`
4. Visit a made-up address like `https://east73studio.com/nope`. You should see "Nothing here."

---

## Optional: keep your email private

GitHub can hide your email in commits. Under GitHub **Settings → Emails**, tick **Keep my email addresses private** and copy the `…@users.noreply.github.com` address shown. Then run:

```bash
git -C C:/Users/sstoo/east73studio-site config user.email "YOUR-ID+YOUR-USERNAME@users.noreply.github.com"
```

This applies to future commits. The handful of commits made before this point keep the old email, so it's best to do this **before** your first push.
