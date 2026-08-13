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

### API

The converter exposes a JSON API:

```bash
curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
  -d '{"text":"HELLO WORLD","seed_word":"TEST","mode":"encrypt"}'
```

## License
This repository/project is licensed under the GNU Affero General Public v3.0-or-later. For more information, please consult the LICENSE file (located in the root of the project), or visit https://www.gnu.org/licenses/agpl-3.0.en.html to read the full license.
