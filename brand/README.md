# core-keys brand

Everything here is **generated**. Do not hand-edit the PNGs — change
`render.py` and re-run it:

```sh
python3 brand/render.py     # needs pillow
```

## Where the mark comes from

It is not a new drawing. It is the device's own boot animation frozen at its
final state: two interlinked rings — the **agent** ring (`#9BB0EE`) over the
**person** ring (`#6D5EF0`) — with the crossings alternating so the pair reads
as one linked chain rather than two stacked circles, and a lit core where they
overlap. Two rings, one core: neither alone is the key.

Geometry and palette are lifted from `draw_rings()` and the `UIC_*` defines in
[core-keys/mule-esp32s3](https://github.com/core-keys/mule-esp32s3)
(`main/ui_screens.c`, `main/ui_screens.h`) — ring radius 40, stroke 13,
separation 30, core discs at 0.62 and 0.34 of the stroke. **If the device UI
changes those, change them here too**, or the printed brand and the thing on
your desk stop matching. The wordmark is Inter SemiBold at +1px tracking, the
same face and tracking the device renders into `img_wordmark`.

## Assets

| file | size | use |
|---|---|---|
| `banner-<repo>.png` | 1600×400 | README header, pinned to `width="800"`. Copied into each repo as `.github/banner.png` by `render.py`. |
| `banner.png` | 1600×400 | the same, without a component label |
| `avatar.png` | 460×460 | organization avatar. Margin is deliberate so a circular crop never clips the rings. |
| `social.png` | 1280×640 | GitHub social preview / og:image (that is GitHub's exact expected size) |
| `mark.png` | 512×512 | mark alone, transparent background |
| `logo.svg` | vector | mark alone. No glow: the lit core is a screen effect for the device's dark panel, and the vector has to stay legible anywhere. |

## Using it

The mark is built for dark backgrounds — that is where the device lives. The
banners and cards therefore carry their own `#080B18` panel, which is why they
look right in both GitHub themes. On a light background use `logo.svg` and
expect the agent ring to be low contrast; darken it rather than putting the
glow back.

`fonts/InterVariable.ttf` is vendored under the SIL Open Font License 1.1 (see
`fonts/LICENSE-Inter.txt`) and is not covered by this project's license.
