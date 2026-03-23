"""
Product Studio — Complete Prompt Library
All 7 themes with 2–4 shots + collage each.
{PRODUCT} is replaced at runtime with the user's product description.
"""

QUALITY_PREFIX = (
    "8K ultra-high-resolution, RAW photograph, photorealistic, hyperdetailed, "
    "no watermark, no text overlay, no logo, no CGI artifacts, sharp focus, "
    "professional commercial photography, "
)

NEGATIVE_PROMPT = (
    "watermark, text, logo, signature, low quality, blurry, cartoon, illustration, "
    "painting, CGI render, 3D render, anime, distorted, deformed, extra objects, "
    "cluttered, ugly, oversaturated, washed out, flat lighting, harsh shadows, "
    "lens flare artifacts, chromatic aberration, grain noise, duplicate objects, "
    "missing parts, wrong proportions"
)

THEMES = {
    "dining": {
        "id": "dining",
        "name": "Dining Elegance",
        "icon": "🍽",
        "concept": "Fine-dining table setting. White linen, candlelight warmth, gold accents.",
        "color": "#C8A96E",
        "shots": [
            {
                "id": "shot_a",
                "label": "Shot A — Hero Solo",
                "type": "Front Elevation · 85mm · f/2.2",
                "prompt": (
                    "studio-quality commercial photograph of {PRODUCT} placed at the center of a fine-dining table setting, "
                    "pure white linen tablecloth with subtle texture, shallow depth of field, "
                    "warm golden candlelight from the left, soft diffused fill light from the right, "
                    "background features elegant bokeh of crystal glassware and folded napkin, "
                    "warm ivory and champagne color palette, neutral tones complement the product's finish, "
                    "camera: 85mm prime lens, f/2.2 aperture, eye-level angle, Hasselblad medium-format style, "
                    "cinematic color grade, deep blacks, lifted highlights, zero noise"
                ),
                "cfg": 7.5, "steps": 50, "sampler": "DPM++ 2M Karras",
            },
            {
                "id": "shot_b",
                "label": "Shot B — Lifestyle Context",
                "type": "3/4 Angle · 50mm · f/2.8",
                "prompt": (
                    "lifestyle commercial photo of {PRODUCT} arranged on a round dining table set for two, "
                    "hand-painted ceramic plates, linen napkins with natural folds, single white peony floral arrangement, "
                    "late afternoon warm window light streaming from upper left, long elegant shadows on the table, "
                    "shallow focus on the product, soft bokeh dining room interior background with timber floors, "
                    "warm amber and cream tones, luxurious yet approachable atmosphere, "
                    "camera: 50mm lens, f/2.8, slight top-down 30-degree tilt, editorial magazine style"
                ),
                "cfg": 7.5, "steps": 50, "sampler": "DPM++ 2M Karras",
            },
            {
                "id": "shot_c",
                "label": "Shot C — Detail Macro",
                "type": "Close-Up · 100mm macro · f/4.0",
                "prompt": (
                    "extreme close-up macro shot of {PRODUCT} resting on a white linen cloth, "
                    "revealing surface texture, finish quality, edge detailing and material craftsmanship, "
                    "single directional soft-box light from the upper right creating delicate rim highlight, "
                    "out-of-focus background hints of candle flame warmth bokeh, "
                    "neutral white and silver color palette with warm temperature, "
                    "camera: 100mm macro lens, f/4.0, tabletop angle, product photography studio style, "
                    "maximum sharpness on product surface, perfectly even exposure"
                ),
                "cfg": 7.5, "steps": 50, "sampler": "DPM++ 2M Karras",
            },
            {
                "id": "shot_d",
                "label": "Shot D — Aerial Flat-Lay",
                "type": "Overhead · 35mm · f/8.0",
                "prompt": (
                    "overhead flat-lay editorial photograph of {PRODUCT} symmetrically arranged on a white marble surface, "
                    "surrounded by dried herbs, linen fabric swatches, and gold cutlery accents as styling props, "
                    "no food, pure product focus, even diffused studio lighting from directly above, "
                    "crisp shadows defining each object edge, pure white background with subtle marble veining, "
                    "camera: 35mm lens, f/8.0, directly overhead bird's eye, magazine editorial flat-lay style, "
                    "perfectly balanced composition, generous negative space"
                ),
                "cfg": 7.5, "steps": 50, "sampler": "DPM++ 2M Karras",
            },
        ],
        "collage_prompt": (
            "4-panel professional product photography collage of {PRODUCT} — dining elegance theme, "
            "top-left: hero front-elevation on white linen tablecloth, "
            "top-right: lifestyle 3/4 angle dining table scene with warm window light, "
            "bottom-left: extreme macro close-up of product surface texture, "
            "bottom-right: overhead flat-lay on white marble with styling props, "
            "consistent warm ivory and champagne color palette across all panels, "
            "clean white dividing lines between panels, no watermarks, no text, "
            "high-end catalog layout, 8K resolution, photorealistic, commercial quality"
        ),
    },

    "kitchen": {
        "id": "kitchen",
        "name": "Kitchen Professional",
        "icon": "🍳",
        "concept": "Modern professional kitchen. Polished stone counters, matte cabinetry, chef-grade context.",
        "color": "#4A7C6F",
        "shots": [
            {
                "id": "shot_a",
                "label": "Shot A — Counter Hero",
                "type": "Marble Counter · 85mm · f/2.5",
                "prompt": (
                    "commercial product photograph of {PRODUCT} placed on a matte Calacatta marble kitchen counter, "
                    "modern handleless dark charcoal cabinets in the background slightly out of focus, "
                    "overhead professional kitchen track lighting from above, secondary soft diffused light from the left, "
                    "cool-toned professional atmosphere with warm accent highlights on the product, "
                    "minimalist kitchen styling with negative space, no food clutter, "
                    "camera: 85mm lens, f/2.5, slight low-angle counter-level, advertising product shot, "
                    "deep rich blacks in shadows, bright catchlights on product surface"
                ),
                "cfg": 7.0, "steps": 45, "sampler": "DPM++ 2M Karras",
            },
            {
                "id": "shot_b",
                "label": "Shot B — In-Use Lifestyle",
                "type": "Natural Light · 50mm · f/2.2",
                "prompt": (
                    "lifestyle photograph of {PRODUCT} in active use on a professional kitchen countertop, "
                    "natural light from a large frosted window on the right, subtle steam context nearby, "
                    "dark green herb sprigs and a linen cloth as minimal props in the background, "
                    "focus locked on the product, background kitchen environment softly blurred, "
                    "muted forest green and off-white color palette complementing the product, "
                    "camera: 50mm lens, f/2.2, straight-on eye-level, editorial food magazine style"
                ),
                "cfg": 7.0, "steps": 45, "sampler": "DPM++ 2M Karras",
            },
            {
                "id": "shot_c",
                "label": "Shot C — Backsplash Wall",
                "type": "Wall Display · 35mm · f/3.5",
                "prompt": (
                    "product photograph of {PRODUCT} displayed against a matte white subway tile backsplash kitchen wall, "
                    "styled as if resting in a storage context, clean and minimal, "
                    "warm under-cabinet LED strip lighting creating a warm golden glow on the product, "
                    "shallow depth of field with very slight blur on surrounding kitchen elements, "
                    "crisp clean aesthetic, neutral whites and warm tones, "
                    "camera: 35mm lens, f/3.5, slightly angled low-to-high shot, interior design editorial style"
                ),
                "cfg": 7.0, "steps": 45, "sampler": "DPM++ 2M Karras",
            },
            {
                "id": "shot_d",
                "label": "Shot D — Dramatic Slate",
                "type": "Dark Stone · 100mm · f/5.6",
                "prompt": (
                    "dramatic low-key studio photo of {PRODUCT} on a dark slate stone surface, "
                    "single overhead spot-light creating sharp specular highlights on the product surface, "
                    "deep dark shadows falling around the product, moody high-contrast atmosphere, "
                    "subtle smoke wisps in the extreme background soft non-distracting, "
                    "near-black background, product finish and material quality the sole visual focus, "
                    "camera: 100mm lens, f/5.6, top-down 45-degree angle, Michelin-star restaurant menu style"
                ),
                "cfg": 7.0, "steps": 45, "sampler": "DPM++ 2M Karras",
            },
        ],
        "collage_prompt": (
            "4-panel professional product photography collage of {PRODUCT} — kitchen professional theme, "
            "top-left: counter hero on Calacatta marble with charcoal cabinets, "
            "top-right: lifestyle in-use shot with natural window light and herbs, "
            "bottom-left: backsplash wall storage context with warm LED lighting, "
            "bottom-right: dramatic dark slate surface with single overhead spotlight, "
            "consistent cool-professional with warm accent color palette across all panels, "
            "clean white dividers, no text, no watermarks, high-end kitchen catalog layout, "
            "8K resolution, photorealistic, commercial quality"
        ),
    },

    "living_room": {
        "id": "living_room",
        "name": "Living Room Lifestyle",
        "icon": "🛋",
        "concept": "Warm Scandinavian living room. Linen textiles, warm wood, afternoon light.",
        "color": "#B07850",
        "shots": [
            {
                "id": "shot_a",
                "label": "Shot A — Coffee Table Hero",
                "type": "Oak Table · 85mm · f/2.0",
                "prompt": (
                    "lifestyle product photograph of {PRODUCT} resting on a light oak coffee table, "
                    "Scandinavian living room background: cream linen sofa, woven throw, dried pampas grass in a vase, "
                    "large window with sheer curtains casting long soft afternoon light across the scene, "
                    "warm golden-hour tones, shallow depth of field, background comfortably out of focus, "
                    "muted warm neutral palette oatmeal sand soft ivory, "
                    "camera: 85mm lens, f/2.0, straight-on tabletop level, lifestyle interior magazine style"
                ),
                "cfg": 7.5, "steps": 50, "sampler": "Euler a",
            },
            {
                "id": "shot_b",
                "label": "Shot B — Shelf Styling",
                "type": "Floating Shelf · 50mm · f/2.8",
                "prompt": (
                    "editorial product photograph of {PRODUCT} styled on a floating white oak shelf in a living room, "
                    "surrounded by a few artfully placed books, a small ceramic vessel, and a trailing plant stem, "
                    "diffused ambient room light from the left, soft shadow on the wall behind, "
                    "warm beige and terracotta accent tones, calm aspirational aesthetic, "
                    "camera: 50mm lens, f/2.8, straight-on shelf-level angle, interior design blog editorial style"
                ),
                "cfg": 7.5, "steps": 50, "sampler": "Euler a",
            },
            {
                "id": "shot_c",
                "label": "Shot C — Hands In-Use",
                "type": "Ritual · 85mm · f/2.0",
                "prompt": (
                    "close-up lifestyle photograph of {PRODUCT} being gently held in a living room context, "
                    "partial view of hands with neutral nail polish and natural skin tone, "
                    "soft natural window light from the right, blurred warm living room background, "
                    "warm skin tones complement the product color palette, "
                    "intimate inviting aspirational product as part of an everyday ritual, "
                    "camera: 85mm lens, f/2.0, side-angle close-up, social media editorial style"
                ),
                "cfg": 7.5, "steps": 50, "sampler": "Euler a",
            },
            {
                "id": "shot_d",
                "label": "Shot D — Window Sill Light",
                "type": "Backlit · 35mm · f/4.0",
                "prompt": (
                    "natural light product photograph of {PRODUCT} placed on a wide painted white window sill, "
                    "golden afternoon sunlight flooding in from behind, soft halo rim light outlining the product, "
                    "sheer linen curtain softly diffusing the light, shadow pattern cast by window frame onto surface, "
                    "minimal styling single dried flower stem no clutter, "
                    "warm backlit glow high-contrast silhouette blending into luminous warmth, "
                    "camera: 35mm lens, f/4.0, slightly low-angle side profile, fine art photography style"
                ),
                "cfg": 7.5, "steps": 50, "sampler": "Euler a",
            },
        ],
        "collage_prompt": (
            "4-panel professional product photography collage of {PRODUCT} — living room lifestyle theme, "
            "top-left: coffee table hero with Scandinavian linen and pampas grass backdrop, "
            "top-right: floating shelf styling with books and ceramic accents, "
            "bottom-left: hands holding product in living room lifestyle context, "
            "bottom-right: window sill natural light rim-lit shot, "
            "consistent warm neutral oatmeal and sand color palette across all panels, "
            "clean white dividers, no text, no watermarks, interior magazine editorial layout, "
            "8K resolution, photorealistic, commercial quality"
        ),
    },

    "alfresco": {
        "id": "alfresco",
        "name": "Outdoor Alfresco",
        "icon": "🌿",
        "concept": "Sun-drenched outdoor dining. Stone terrace, Mediterranean herbs, dappled shade.",
        "color": "#6B8C5A",
        "shots": [
            {
                "id": "shot_a",
                "label": "Shot A — Stone Terrace",
                "type": "Mediterranean · 85mm · f/2.5",
                "prompt": (
                    "outdoor lifestyle product photograph of {PRODUCT} on a weathered stone terrace dining table, "
                    "Mediterranean alfresco setting terracotta pots with rosemary and lavender in the soft background, "
                    "dappled sunlight filtering through olive tree leaves casting organic shadow patterns on the surface, "
                    "warm golden midday sun from the upper left, product well-lit with no harsh overexposure, "
                    "warm sandy stone and muted sage green color palette, "
                    "camera: 85mm lens, f/2.5, straight-on table level, architectural digest outdoor editorial style"
                ),
                "cfg": 8.0, "steps": 55, "sampler": "DPM++ SDE Karras",
            },
            {
                "id": "shot_b",
                "label": "Shot B — Garden Flat-Lay",
                "type": "Picnic Cloth · 35mm · f/6.3",
                "prompt": (
                    "top-down flat-lay photograph of {PRODUCT} placed on a linen picnic cloth in a garden setting, "
                    "fresh green grass visible at the edges, scattered wildflowers and a folded linen napkin as props, "
                    "bright even outdoor diffused light slightly overcast sky for perfect soft light no harsh shadows, "
                    "vibrant natural greens complementing product tones, fresh summer atmosphere, "
                    "camera: 35mm lens, f/6.3, directly overhead, Kinfolk magazine picnic editorial style"
                ),
                "cfg": 8.0, "steps": 55, "sampler": "DPM++ SDE Karras",
            },
            {
                "id": "shot_c",
                "label": "Shot C — Dusk Candlelight",
                "type": "Twilight · 85mm · f/2.0",
                "prompt": (
                    "twilight outdoor photograph of {PRODUCT} on a stone terrace table lit by candlelight and string lights, "
                    "warm amber and deep indigo sky gradient in the background, candles flickering softly, "
                    "warm light on the product surface perfect detail retention, "
                    "intimate alfresco dinner atmosphere no other people product is the visual anchor, "
                    "camera: 85mm lens, f/2.0, low table-level angle, travel lifestyle magazine evening editorial"
                ),
                "cfg": 8.0, "steps": 55, "sampler": "DPM++ SDE Karras",
            },
        ],
        "collage_prompt": (
            "3-panel professional product photography collage of {PRODUCT} — outdoor alfresco theme, "
            "left: stone terrace table with Mediterranean herbs and dappled sunlight, "
            "center: overhead garden flat-lay on linen cloth with wildflowers, "
            "right: dusk terrace candlelight and string lights bokeh, "
            "consistent warm stone and sage green color palette across all panels, "
            "clean thin white dividers, no text, no watermarks, travel lifestyle editorial layout, "
            "8K resolution, photorealistic, commercial quality"
        ),
    },

    "spa": {
        "id": "spa",
        "name": "Spa & Wellness",
        "icon": "🕯",
        "concept": "Serene spa bathroom. White towels, eucalyptus, stone surfaces, soft morning light.",
        "color": "#9AACA8",
        "shots": [
            {
                "id": "shot_a",
                "label": "Shot A — Marble Vanity",
                "type": "Carrara Marble · 85mm · f/2.8",
                "prompt": (
                    "commercial product photograph of {PRODUCT} arranged on a white Carrara marble vanity surface, "
                    "minimal spa styling: rolled white towel beside the product, fresh eucalyptus sprig, "
                    "soft diffused morning light from a frosted glass window on the left, gentle catchlight on product, "
                    "pure white and pale grey marble tones, ultra-clean minimalist aesthetic, "
                    "camera: 85mm lens, f/2.8, straight-on counter-level, luxury hotel amenity photography style"
                ),
                "cfg": 6.5, "steps": 45, "sampler": "DPM++ 2M Karras",
            },
            {
                "id": "shot_b",
                "label": "Shot B — Steam Room",
                "type": "Moody Backlit · 50mm · f/2.5",
                "prompt": (
                    "atmospheric product photograph of {PRODUCT} on a smooth pebble stone surface in a spa-inspired setting, "
                    "warm backlighting creating a soft ethereal glow through thin steam wisps in the background, "
                    "dark charcoal stone and warm candlelight accents, high contrast moody wellness aesthetic, "
                    "product sharply in focus, background pleasantly diffused, "
                    "camera: 50mm lens, f/2.5, low side-angle, luxury spa brand visual identity style"
                ),
                "cfg": 6.5, "steps": 45, "sampler": "DPM++ 2M Karras",
            },
        ],
        "collage_prompt": (
            "2-panel professional product photography collage of {PRODUCT} — spa and wellness theme, "
            "left: white Carrara marble vanity with eucalyptus and rolled towel morning light, "
            "right: pebble stone surface with ethereal steam backlighting and warm candlelight, "
            "consistent pale marble and warm charcoal tones across both panels, "
            "clean minimal white divider, no text, no watermarks, luxury wellness brand catalog layout, "
            "8K resolution, photorealistic, commercial quality"
        ),
    },

    "studio": {
        "id": "studio",
        "name": "Minimalist Studio",
        "icon": "◻",
        "concept": "Pure infinity cyc studio. No environment context. Product is everything.",
        "color": "#888888",
        "shots": [
            {
                "id": "shot_a",
                "label": "Shot A — White Infinity",
                "type": "3-Point Lit · 100mm · f/8.0",
                "prompt": (
                    "professional studio product photograph of {PRODUCT} on a pure seamless white infinity curve background, "
                    "three-point studio lighting: key light upper-left soft-box, fill light from right, rim light from behind, "
                    "zero shadows visible on the background, product suspended in clean white space, "
                    "all surface details textures and finishes of the product are perfectly resolved, "
                    "camera: 100mm lens, f/8.0, perfectly straight-on eye level, e-commerce hero shot style"
                ),
                "cfg": 6.0, "steps": 40, "sampler": "DDIM",
            },
            {
                "id": "shot_b",
                "label": "Shot B — Grey Gradient",
                "type": "Octabox · 85mm · f/6.3",
                "prompt": (
                    "studio product photograph of {PRODUCT} centered on a smooth light grey gradient background, "
                    "soft natural gradient from near-white behind the product to mid-grey at the edges, "
                    "single large overhead octabox light source, subtle drop shadow on the surface below, "
                    "product occupies the central third of the frame, generous breathing room on all sides, "
                    "camera: 85mm lens, f/6.3, straight-on level, Amazon premium listing hero image style"
                ),
                "cfg": 6.0, "steps": 40, "sampler": "DDIM",
            },
            {
                "id": "shot_c",
                "label": "Shot C — Dark Moody",
                "type": "Rim Lit · 85mm · f/5.6",
                "prompt": (
                    "moody low-key studio product photograph of {PRODUCT} on a dark charcoal seamless background, "
                    "single directional rim light from upper right creating sharp specular edges on the product, "
                    "deep dramatic shadows, strong contrast, premium brand visual identity aesthetic, "
                    "product surface and material quality maximally showcased, "
                    "camera: 85mm lens, f/5.6, 3/4 angle from slightly above, luxury brand catalog style"
                ),
                "cfg": 6.0, "steps": 40, "sampler": "DDIM",
            },
        ],
        "collage_prompt": (
            "3-panel professional product photography collage of {PRODUCT} — minimalist studio theme, "
            "left: pure seamless white infinity background three-point studio lighting e-commerce hero, "
            "center: light grey gradient overhead octabox generous negative space, "
            "right: dark charcoal background single rim light dramatic low-key moody studio, "
            "no text, no watermarks, clean product catalog layout with thin white borders, "
            "8K resolution, photorealistic, commercial quality"
        ),
    },

    "cafe": {
        "id": "cafe",
        "name": "Boutique Café",
        "icon": "☕",
        "concept": "Specialty coffee shop. Exposed brick, warm timber, hand-thrown ceramics.",
        "color": "#8B5E3C",
        "shots": [
            {
                "id": "shot_a",
                "label": "Shot A — Café Counter",
                "type": "Reclaimed Timber · 85mm · f/2.2",
                "prompt": (
                    "lifestyle product photograph of {PRODUCT} displayed on a reclaimed timber café counter, "
                    "exposed brick wall background, artisan ceramic coffee cups beside the product as styling props, "
                    "warm tungsten pendant light from above, secondary soft light from a nearby window, "
                    "warm amber and terracotta palette, artisan craft aesthetic, no cluttered background, "
                    "camera: 85mm lens, f/2.2, counter-level straight-on, specialty coffee brand editorial style"
                ),
                "cfg": 7.5, "steps": 50, "sampler": "Euler a",
            },
            {
                "id": "shot_b",
                "label": "Shot B — Marble Café Table",
                "type": "Morning Light · 50mm · f/2.0",
                "prompt": (
                    "café lifestyle photograph of {PRODUCT} resting on a small round marble café table, "
                    "a single espresso cup placed a short distance away out of focus, morning light from a tall window, "
                    "newspaper softly blurred in the background, warm morning ambiance, "
                    "warm cream marble surface, soft natural light, café culture aspirational aesthetic, "
                    "camera: 50mm lens, f/2.0, eye-level slight bird's eye, Kinfolk magazine editorial style"
                ),
                "cfg": 7.5, "steps": 50, "sampler": "Euler a",
            },
        ],
        "collage_prompt": (
            "2-panel professional product photography collage of {PRODUCT} — boutique café theme, "
            "left: reclaimed timber counter with exposed brick and tungsten pendant light, "
            "right: marble café table with espresso cup and morning window light, "
            "consistent warm amber and cream color palette, "
            "clean minimal divider, no text, no watermarks, specialty food beverage catalog layout, "
            "8K resolution, photorealistic, commercial quality"
        ),
    },
}


def build_prompt(template: str, product_description: str) -> str:
    """Build a complete positive prompt from a template and product description."""
    return QUALITY_PREFIX + template.replace("{PRODUCT}", product_description)


def get_theme(theme_id: str) -> dict:
    return THEMES.get(theme_id)


def get_all_themes() -> list:
    return list(THEMES.values())
