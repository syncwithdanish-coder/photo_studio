"""
All 7 themes × shots × prompts.
{PRODUCT} is replaced at runtime.
"""

QUALITY = (
    "8K ultra-high-resolution, RAW photograph, photorealistic, hyperdetailed, "
    "no watermark, no text, no logo, no CGI artifacts, sharp focus, "
    "professional commercial photography, "
)

NEGATIVE = (
    "watermark, text, logo, signature, blurry, cartoon, CGI, 3D render, "
    "distorted, deformed, ugly, oversaturated, flat lighting, grain noise, "
    "duplicate objects, wrong proportions, missing parts, nsfw"
)

THEMES = {
    "dining": {
        "name":    "Dining Elegance",
        "icon":    "🍽",
        "concept": "Fine-dining table. White linen, candlelight, gold accents.",
        "color":   "#c8a96e",
        "bg":      "#2a1e10",
        "shots": [
            {
                "id":     "shot_a",
                "label":  "Hero Shot",
                "type":   "Front · 85mm · f/2.2",
                "prompt": (
                    "studio-quality commercial photograph of {PRODUCT} at the center of a "
                    "fine-dining table, white linen tablecloth, warm golden candlelight from "
                    "the left, soft bokeh of crystal glassware in background, ivory and champagne "
                    "palette, 85mm f/2.2, Hasselblad medium-format, cinematic color grade"
                ),
            },
            {
                "id":     "shot_b",
                "label":  "Lifestyle",
                "type":   "3/4 · 50mm · f/2.8",
                "prompt": (
                    "lifestyle photo of {PRODUCT} on a round dining table set for two, "
                    "ceramic plates, white peony, late afternoon window light, shallow focus, "
                    "timber floor bokeh, warm amber tones, 50mm f/2.8 editorial magazine style"
                ),
            },
            {
                "id":     "shot_c",
                "label":  "Detail Macro",
                "type":   "Macro · 100mm · f/4",
                "prompt": (
                    "extreme close-up macro of {PRODUCT} on white linen, revealing surface "
                    "texture and material craftsmanship, soft-box rim light, candle bokeh, "
                    "100mm macro f/4, maximum sharpness, white silver warm palette"
                ),
            },
            {
                "id":     "shot_d",
                "label":  "Flat-Lay",
                "type":   "Overhead · 35mm · f/8",
                "prompt": (
                    "overhead flat-lay of {PRODUCT} on white marble, dried herbs and gold "
                    "accents as props, even diffused studio light, crisp shadows, 35mm f/8, "
                    "magazine editorial, generous negative space"
                ),
            },
        ],
        "collage_prompt": (
            "4-panel product photography collage of {PRODUCT}, dining elegance theme: "
            "top-left hero on white linen, top-right lifestyle dining scene, "
            "bottom-left macro surface detail, bottom-right overhead marble flat-lay, "
            "ivory and champagne palette, no watermarks, commercial quality"
        ),
    },

    "kitchen": {
        "name":    "Kitchen Professional",
        "icon":    "🍳",
        "concept": "Modern pro kitchen. Marble counter, dark cabinets.",
        "color":   "#7ab8a0",
        "bg":      "#121e1a",
        "shots": [
            {
                "id":     "shot_a",
                "label":  "Counter Hero",
                "type":   "Low angle · 85mm · f/2.5",
                "prompt": (
                    "commercial photo of {PRODUCT} on Calacatta marble counter, dark charcoal "
                    "cabinets soft background, overhead track lighting, cool tones with warm "
                    "accent highlights, 85mm f/2.5 low angle, advertising shot"
                ),
            },
            {
                "id":     "shot_b",
                "label":  "In-Use",
                "type":   "Natural light · 50mm · f/2.2",
                "prompt": (
                    "lifestyle photo of {PRODUCT} in use on kitchen counter, frosted window "
                    "light from right, dark green herb sprigs as props, forest green palette, "
                    "50mm f/2.2 food magazine style"
                ),
            },
            {
                "id":     "shot_c",
                "label":  "Dark Slate",
                "type":   "Dramatic · 100mm · f/5.6",
                "prompt": (
                    "dramatic low-key photo of {PRODUCT} on dark slate, single overhead "
                    "spotlight, sharp specular highlights, deep shadows, near-black background, "
                    "100mm f/5.6 Michelin-style"
                ),
            },
        ],
        "collage_prompt": (
            "3-panel kitchen product collage of {PRODUCT}: "
            "left marble counter hero, center in-use natural light, right dark slate dramatic, "
            "professional kitchen aesthetic, no watermarks"
        ),
    },

    "living_room": {
        "name":    "Living Room",
        "icon":    "🛋",
        "concept": "Warm Scandinavian living room. Oak, linen, afternoon light.",
        "color":   "#c89060",
        "bg":      "#201408",
        "shots": [
            {
                "id":     "shot_a",
                "label":  "Coffee Table",
                "type":   "85mm · f/2.0",
                "prompt": (
                    "lifestyle photo of {PRODUCT} on light oak coffee table, cream linen sofa "
                    "and pampas grass in background, golden afternoon window light, warm oatmeal "
                    "palette, 85mm f/2.0 interior magazine"
                ),
            },
            {
                "id":     "shot_b",
                "label":  "Shelf Styling",
                "type":   "50mm · f/2.8",
                "prompt": (
                    "editorial photo of {PRODUCT} on floating oak shelf with books and ceramic "
                    "vessel, ambient room light, beige terracotta tones, 50mm f/2.8 interior "
                    "design blog"
                ),
            },
            {
                "id":     "shot_c",
                "label":  "Window Sill",
                "type":   "Backlit · 35mm · f/4",
                "prompt": (
                    "natural light photo of {PRODUCT} on white window sill, golden afternoon "
                    "backlight creating rim light, sheer linen curtain, single dried flower stem, "
                    "35mm f/4 fine art style"
                ),
            },
        ],
        "collage_prompt": (
            "3-panel living room lifestyle collage of {PRODUCT}: "
            "left coffee table golden hour, center shelf styling, right window sill backlit, "
            "warm neutral Scandinavian palette, no watermarks"
        ),
    },

    "alfresco": {
        "name":    "Outdoor Alfresco",
        "icon":    "🌿",
        "concept": "Mediterranean terrace. Stone, herbs, dappled sun.",
        "color":   "#90c870",
        "bg":      "#101808",
        "shots": [
            {
                "id":     "shot_a",
                "label":  "Stone Terrace",
                "type":   "85mm · f/2.5",
                "prompt": (
                    "outdoor photo of {PRODUCT} on weathered stone terrace table, terracotta "
                    "pots with rosemary in background, dappled olive tree sunlight, sandy stone "
                    "and sage green palette, 85mm f/2.5 architectural digest"
                ),
            },
            {
                "id":     "shot_b",
                "label":  "Garden Flat-Lay",
                "type":   "Overhead · 35mm · f/6.3",
                "prompt": (
                    "overhead flat-lay of {PRODUCT} on linen picnic cloth, green grass at edges, "
                    "scattered wildflowers, soft overcast light, 35mm f/6.3 Kinfolk style"
                ),
            },
            {
                "id":     "shot_c",
                "label":  "Dusk Candles",
                "type":   "Twilight · 85mm · f/2.0",
                "prompt": (
                    "twilight photo of {PRODUCT} on stone table, candlelight and string lights, "
                    "warm amber and indigo sky, intimate dinner atmosphere, 85mm f/2.0 travel "
                    "magazine"
                ),
            },
        ],
        "collage_prompt": (
            "3-panel alfresco collage of {PRODUCT}: "
            "left stone terrace Mediterranean, center garden flat-lay, right dusk candlelight, "
            "warm stone and sage palette, no watermarks"
        ),
    },

    "spa": {
        "name":    "Spa & Wellness",
        "icon":    "🕯",
        "concept": "Luxury spa. Marble, eucalyptus, morning light.",
        "color":   "#a0c8c8",
        "bg":      "#0c1818",
        "shots": [
            {
                "id":     "shot_a",
                "label":  "Marble Vanity",
                "type":   "85mm · f/2.8",
                "prompt": (
                    "commercial photo of {PRODUCT} on white Carrara marble vanity, rolled white "
                    "towel and eucalyptus sprig, frosted glass morning light, pale grey marble, "
                    "85mm f/2.8 luxury hotel"
                ),
            },
            {
                "id":     "shot_b",
                "label":  "Moody Backlit",
                "type":   "50mm · f/2.5",
                "prompt": (
                    "atmospheric photo of {PRODUCT} on pebble stone surface, warm backlight "
                    "through thin steam, dark charcoal tones, candlelight accents, 50mm f/2.5 "
                    "luxury spa visual identity"
                ),
            },
        ],
        "collage_prompt": (
            "2-panel spa collage of {PRODUCT}: "
            "left marble vanity morning light, right pebble stone steam backlit, "
            "pale marble and charcoal palette, no watermarks"
        ),
    },

    "studio": {
        "name":    "Clean Studio",
        "icon":    "◻",
        "concept": "Pure studio. Product is everything.",
        "color":   "#c0c0c0",
        "bg":      "#141414",
        "shots": [
            {
                "id":     "shot_a",
                "label":  "White Infinity",
                "type":   "100mm · f/8 · 3-point lit",
                "prompt": (
                    "studio product photo of {PRODUCT} on pure seamless white infinity curve, "
                    "3-point lighting: key soft-box left, fill right, rim behind, zero visible "
                    "shadows, 100mm f/8 e-commerce hero"
                ),
            },
            {
                "id":     "shot_b",
                "label":  "Grey Gradient",
                "type":   "85mm · f/6.3 · octabox",
                "prompt": (
                    "product photo of {PRODUCT} on light grey gradient, octabox overhead, "
                    "subtle drop shadow, generous breathing room, 85mm f/6.3 premium listing"
                ),
            },
            {
                "id":     "shot_c",
                "label":  "Dark Moody",
                "type":   "85mm · f/5.6 · rim lit",
                "prompt": (
                    "moody studio photo of {PRODUCT} on dark charcoal, single rim light from "
                    "upper right, deep shadows, premium brand aesthetic, 85mm f/5.6"
                ),
            },
        ],
        "collage_prompt": (
            "3-panel studio collage of {PRODUCT}: "
            "left white infinity hero, center grey gradient, right dark moody, "
            "clean minimal layout, no watermarks"
        ),
    },

    "cafe": {
        "name":    "Boutique Café",
        "icon":    "☕",
        "concept": "Specialty coffee shop. Timber, exposed brick, ceramics.",
        "color":   "#c07840",
        "bg":      "#180c04",
        "shots": [
            {
                "id":     "shot_a",
                "label":  "Timber Counter",
                "type":   "85mm · f/2.2",
                "prompt": (
                    "lifestyle photo of {PRODUCT} on reclaimed timber café counter, exposed brick "
                    "background, artisan ceramic cups, tungsten pendant light, amber palette, "
                    "85mm f/2.2 specialty coffee brand"
                ),
            },
            {
                "id":     "shot_b",
                "label":  "Café Table",
                "type":   "50mm · f/2.0",
                "prompt": (
                    "café photo of {PRODUCT} on small round marble café table, espresso cup "
                    "out-of-focus nearby, morning window light, warm cream marble, 50mm f/2.0 "
                    "Kinfolk editorial"
                ),
            },
        ],
        "collage_prompt": (
            "2-panel café collage of {PRODUCT}: "
            "left timber counter exposed brick, right marble café table morning light, "
            "warm amber and cream palette, no watermarks"
        ),
    },
}


def build_prompt(template: str, product: str) -> str:
    return QUALITY + template.replace("{PRODUCT}", product)


def get_theme(tid: str) -> dict:
    return THEMES[tid]


def all_themes() -> list[dict]:
    return list(THEMES.values())
