Clipper is a first-of-its-kind encryption suite, which makes it virtually impossible for an encoded message to be cracked through traditional means.

A seed word is entered, which generates a 52 digit long seed. The seed is generated is consistent to the word, and not random.

The CVC (Clipper Variable Cipherkey) system is a derivative of a polyalphabetic cipher, similar to the encryption system "Enigma."

The word can be decrypted if someone has the seed word which was used to encrypt it, and Clipper itself.

For a full writeup, visit [https://ayriknabirahni.com/writeup/clipper-encryption/](https://ayriknabirahni.com/writeup/clipper-encryption/).

## Docker Compose web app

This repository now includes a simple Flask-based web interface and Docker Compose setup so it can be run as a browser app or embedded into another page.

### Run locally

```bash
docker compose up --build
```

Then open:

- http://localhost:5000/
- http://localhost:5000/embed
- http://localhost:5000/health

### Embed

Use the `/embed` route inside an iframe. The embedded app sends `clipper-web:resize`
messages so the parent page can hide its loader and resize the frame.

```html
<div class="clipper-web-frame-wrap">
  <div class="clipper-web-loader" id="clipper-web-loader">
    <span></span>
    <strong>Loading converter...</strong>
  </div>

  <iframe
    id="clipper-web-converter"
    src="https://your-domain.example/embed"
    title="clipper-web text converter"
    loading="lazy"
  ></iframe>
</div>

<script>
const clipperWebIframe = document.getElementById("clipper-web-converter");
const clipperWebLoader = document.getElementById("clipper-web-loader");
const clipperWebLoaderText = clipperWebLoader ? clipperWebLoader.querySelector("strong") : null;
const clipperWebOrigin = new URL(clipperWebIframe.src, window.location.href).origin;
const clipperWebMaxRetries = 3;
const clipperWebRetryDelayMs = 7000;
let clipperWebRetryCount = 0;
let clipperWebReady = false;
let clipperWebRetryTimer = null;

function showClipperWebFrame() {
  clipperWebReady = true;
  window.clearTimeout(clipperWebRetryTimer);
  if (clipperWebLoader) clipperWebLoader.hidden = true;
  if (clipperWebIframe) clipperWebIframe.classList.add("is-loaded");
}

function resetClipperWebFrame() {
  if (!clipperWebIframe || clipperWebReady) return;

  if (clipperWebRetryCount >= clipperWebMaxRetries) {
    if (clipperWebLoaderText) {
      clipperWebLoaderText.textContent = "Converter is taking longer than expected. Refresh this page to try again.";
    }
    return;
  }

  clipperWebRetryCount += 1;
  if (clipperWebLoaderText) {
    clipperWebLoaderText.textContent = `Retrying converter... (${clipperWebRetryCount}/${clipperWebMaxRetries})`;
  }

  const nextUrl = new URL(clipperWebIframe.src);
  nextUrl.searchParams.set("retry", Date.now().toString());
  clipperWebIframe.classList.remove("is-loaded");
  clipperWebIframe.src = nextUrl.toString();
  startClipperWebWatchdog();
}

function startClipperWebWatchdog() {
  window.clearTimeout(clipperWebRetryTimer);
  clipperWebRetryTimer = window.setTimeout(resetClipperWebFrame, clipperWebRetryDelayMs);
}

window.addEventListener("message", event => {
  if (event.origin !== clipperWebOrigin) return;
  if (!event.data || event.data.type !== "clipper-web:resize") return;

  showClipperWebFrame();
  if (clipperWebIframe) {
    clipperWebIframe.style.height = `${Math.max(360, Math.min(event.data.height, 1600))}px`;
  }
});

startClipperWebWatchdog();
</script>

<style>
.clipper-web-frame-wrap {
  position: relative;
  width: 100%;
  min-height: 360px;
}

#clipper-web-converter {
  display: block;
  width: 100%;
  height: 520px;
  border: 0;
  opacity: 0;
  transition: opacity 180ms ease;
}

#clipper-web-converter.is-loaded {
  opacity: 1;
}

.clipper-web-loader {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: grid;
  place-items: center;
  gap: 12px;
  align-content: center;
  min-height: 360px;
  border: 1px solid #303942;
  border-radius: 8px;
  background: #090c10;
  color: #f4f7f8;
  font: 16px/1.4 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.clipper-web-loader span {
  width: 34px;
  height: 34px;
  border: 3px solid rgba(249, 0, 0, 0.24);
  border-top-color: #f90000;
  border-radius: 50%;
  animation: clipper-web-spin 800ms linear infinite;
}

.clipper-web-loader[hidden] {
  display: none;
}

@keyframes clipper-web-spin {
  to { transform: rotate(360deg); }
}
</style>
```

### API

The converter exposes a JSON API:

```bash
curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
  -d '{"text":"HELLO WORLD","seed_word":"TEST","mode":"encrypt"}'
```

The API response includes `result` plus a `trace` array with the seed, word, and
letter-level conversion steps shown in the web console.

## License
This repository/project is licensed under the GNU Affero General Public v3.0-or-later. For more information, please consult the LICENSE file (located in the root of the project), or visit https://www.gnu.org/licenses/agpl-3.0.en.html to read the full license.
