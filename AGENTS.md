# Threadlocked site design grammar

- Edit the committed HTML, `style.css`, and assets directly. Keep the author's wording and page structure unless a request explicitly changes them.
- GitHub Pages publishes the root of `main`. Keep `CNAME` set to `threadlocked.xyz` and `.nojekyll` at the root.
- Use a quiet, text-first, single-column reading layout: Georgia, 17px body text, 1.6 line height, `#292929` text, `#f5f5f5` background, and `#1656cc` links. Keep the reading column at 640px maximum.
- Keep headings in Georgia at normal weight with a clear hierarchy: `h1` 1.4em, `h2` 1.2em, `h3` 1em. Strong emphasis is italic at normal weight.
- The root page shows no icons before links. Same-site links and Google Forms links show no icons on any page. Other external links, including email links, use a small local favicon when available; keep the icon decorative with empty alt text.
- Use `favicons/threadlocked.png` as the site icon for every page on the Threadlocked domain, including Rabbit Holes.
- Use descriptive link text. Preserve target URLs and spell the creative coding library `p5.js` in prose.
- Keep article images responsive within the reading column. Use 640px and 1280px variants with `srcset`, `sizes`, intrinsic dimensions, lazy loading, and informative alt text. Editorial images use captions.
- Check all changed pages and local links and images before committing.
- Use Conventional Commits for commit subjects, such as `feat: add a page`, `fix: correct a link`, or `chore: update repository files`.
