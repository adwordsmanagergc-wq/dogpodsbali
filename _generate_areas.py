#!/usr/bin/env python3
"""Generate location-specific dog pod landing pages for SEO."""
import os, json, re

AREAS = [
    {
        "slug": "canggu",
        "name": "Canggu",
        "tagline": "From Echo Beach to Berawa — your dog rides too",
        "intro": (
            "Canggu is where most Bali dog pods end up — and it's not hard to see why. "
            "Between the narrow gangs (lanes), the constant traffic on Pantai Berawa, the "
            "crawl up to Echo Beach at sunset and the dog-friendly café scene around Babi "
            "Guling Pererenan and Crate, getting around with a dog by any means other than "
            "scooter is genuinely impractical. A custom dog pod fitted to your Vario, NMAX or "
            "PCX turns Canggu's daily chaos into something your dog can actually be part of."
        ),
        "spots": [
            ("Echo Beach &amp; Batu Bolong", "Sunset surf-checks with your dog watching from the pod, then dinner at La Brisa or Old Man's."),
            ("Berawa &amp; Pantai Berawa", "Beach Canyon Club, Atlas, Finns — most are dog-tolerant outside, and the bike traffic means a pod is the only sane way to get there."),
            ("Pererenan border", "Quieter rice-field tracks, perfect for a morning ride before the heat."),
            ("Babi Guling Mertha Sari &amp; the warung run", "School run, vet run, coffee run — daily errands the pod makes possible."),
        ],
        "delivery": "Bike pickup &amp; drop-off available across the Canggu / Berawa / Pererenan triangle (extra IDR 450,000–750,000 depending on location).",
        "neighbours": ["pererenan", "seminyak", "denpasar"],
    },
    {
        "slug": "ubud",
        "name": "Ubud",
        "tagline": "Rice paddies, jungle hills and the dog who comes too",
        "intro": (
            "Ubud is hilly, hot, and laced with one-way streets that make car ownership feel "
            "ridiculous. Almost everyone — Balinese and expat — runs a 125 or 150cc scooter, "
            "and once you've adopted a dog from BAWA, Mission Pawsible or one of the local "
            "shelters, you suddenly need a way to bring them with you. A Dharma's Dog Pod, "
            "built around your bike and your dog, is the difference between leaving your dog "
            "at the villa and taking them up to Tegallalang for a ride through the rice fields."
        ),
        "spots": [
            ("Penestanan &amp; Sayan", "The hilly expat hubs where most Ubud dog parents live — narrow lanes, scooter-only parking."),
            ("Tegallalang &amp; Kintamani roads", "Cool morning rides up into the highlands with your dog watching the rice terraces fly past."),
            ("Monkey Forest Road &amp; Hanoman", "Daily café and warung runs — Café Pomegranate, Yellow Flower, Earth Café."),
            ("Local vets &amp; rescues", "Sunset Vet Ubud, BAWA, The Sunrise School Sanctuary — easy access with the dog in the pod."),
        ],
        "delivery": "Bike pickup &amp; drop-off across Ubud, Penestanan, Sayan and surrounding banjars (extra IDR 450,000–750,000 depending on location).",
        "neighbours": ["denpasar", "sanur", "canggu"],
    },
    {
        "slug": "uluwatu",
        "name": "Uluwatu",
        "tagline": "Cliffs, surf and the easiest way to take your dog with you",
        "intro": (
            "Uluwatu's cliff roads and steep clifftop villas mean a scooter isn't really "
            "optional — and the long, hot stretches between Padang Padang, Bingin, Suluban and "
            "Nyang Nyang make it impossible to walk a dog there safely. A custom dog pod "
            "fitted to your bike turns the Bukit Peninsula from a place where you leave the "
            "dog at home into a place you ride together at sunset, with the pod's clear "
            "acrylic window keeping them shaded but in on the view."
        ),
        "spots": [
            ("Padang Padang &amp; Bingin", "Surf checks, sunset beers at Single Fin, dinner at The Cashew Tree."),
            ("Pecatu &amp; Pandawa", "The quieter side of the Bukit — steep access roads where a properly mounted pod really shows its worth."),
            ("Uluwatu Temple road", "Iconic clifftop ride with the dog watching the limestone go past."),
            ("Suluban &amp; Nyang Nyang", "Dirt-track approaches that wreck cheap pods — fibreglass holds up where ply doesn't."),
        ],
        "delivery": "Bike pickup &amp; drop-off across the Bukit — Uluwatu, Pecatu, Bingin, Ungasan, Jimbaran (extra IDR 450,000–750,000 depending on location).",
        "neighbours": ["denpasar", "seminyak", "sanur"],
    },
    {
        "slug": "seminyak",
        "name": "Seminyak",
        "tagline": "Petitenget to Beachwalk, with your best mate on the bike",
        "intro": (
            "Seminyak's traffic is some of the worst in Bali, and parking near Petitenget, "
            "Beachwalk or Eat Street is genuinely a nightmare. That's why scooters dominate "
            "and dog pods are increasingly common — they're the only way to take a dog to "
            "dinner at La Lucciola or a sunset at Potato Head without leaving them home alone "
            "for half the evening. Dharma builds and fits pods to any bike, in any colour, "
            "delivered into Seminyak."
        ),
        "spots": [
            ("Petitenget &amp; Eat Street", "Dinner runs to Sisterfields, La Lucciola, Mama San — pod parks anywhere a bike does."),
            ("Beachwalk &amp; Kuta border", "Easy access to vets and dog supply stores in Kuta and Legian."),
            ("Pantai Seminyak", "Sunset beach trips — drainage holes mean the sand washes straight out."),
            ("Drupadi area", "Cheap parking, narrow lanes, scooter-only territory."),
        ],
        "delivery": "Bike pickup &amp; drop-off throughout Seminyak, Kerobokan, Petitenget and Legian (extra IDR 450,000–750,000 depending on location).",
        "neighbours": ["canggu", "denpasar", "pererenan"],
    },
    {
        "slug": "pererenan",
        "name": "Pererenan",
        "tagline": "Bali's quieter dog-loving neighbourhood",
        "intro": (
            "Pererenan has quietly become one of Bali's most dog-loving neighbourhoods — calmer "
            "than Canggu, more residential than Seminyak, with rice-field tracks that are "
            "actually rideable. Most of the new villas here are built around scooters, not "
            "cars, and almost every long-stay resident ends up adopting a dog. A Dharma's Dog "
            "Pod fitted to your bike makes Pererenan's daily rhythm — beach in the morning, "
            "café midday, sunset at La Brisa — actually doable with your dog along for the "
            "ride."
        ),
        "spots": [
            ("Pantai Pererenan", "The least-crowded surf beach in the Canggu cluster — perfect dog-pod sunsets."),
            ("Wanagiri &amp; Tibubeneng", "Quiet back roads where you can practise riding with the pod loaded."),
            ("Babi Guling Mertha Sari &amp; warung run", "Daily errands without leaving the dog behind."),
            ("La Brisa / Atlas / The Lawn", "All a short pod ride away."),
        ],
        "delivery": "Bike pickup &amp; drop-off across Pererenan, Wanagiri, Tibubeneng and the Canggu border (extra IDR 450,000–750,000 depending on location).",
        "neighbours": ["canggu", "seminyak", "denpasar"],
    },
    {
        "slug": "denpasar",
        "name": "Denpasar",
        "tagline": "Bali's capital — where the vets are and the bike-life is real",
        "intro": (
            "Denpasar is where Bali's local life happens — and where most of the island's "
            "best vets, pet supply stores and rescue organisations are based. If you live in "
            "Denpasar, riding a scooter isn't a lifestyle choice — it's just how you get to "
            "work. Adding a dog pod to that bike means your dog gets to come to the vet, the "
            "pet shop, the family warung visit, without you having to organise a Grab car "
            "every time."
        ),
        "spots": [
            ("Renon &amp; Niti Mandala", "Big roads, residential life, daily routine — pod-friendly."),
            ("Sanglah area", "Vet hub of Bali — Sunset Vet, Bali Pet Crusaders, Pet Crew."),
            ("Sesetan &amp; Pemogan", "Local neighbourhoods where pods stand out and scooters dominate."),
            ("Sidakarya &amp; Pedungan", "Easy access to Sanur and the bypass."),
        ],
        "delivery": "Bike pickup &amp; drop-off available across Denpasar (extra IDR 450,000–750,000 depending on location).",
        "neighbours": ["sanur", "ubud", "seminyak"],
    },
    {
        "slug": "sanur",
        "name": "Sanur",
        "tagline": "Sunrise rides on the east coast — with your dog along for it",
        "intro": (
            "Sanur is Bali's gentler, slower east coast — long beach paths, retired expats, "
            "early-morning sunrise rides. The dog community here skews older and more settled, "
            "but the practical problem is identical to Canggu's: scooters are the default, and "
            "without a proper pod you can't bring your dog along. Dharma fits pods all over "
            "Sanur, from the Mertasari beach end to the bypass, in any colour to match your "
            "bike."
        ),
        "spots": [
            ("Pantai Sanur &amp; the boardwalk", "Sunrise rides with the dog watching the sea."),
            ("Mertasari &amp; Semawang", "Quiet residential back lanes, scooter-only territory."),
            ("Bypass Ngurah Rai &amp; Renon", "Quick connection to Denpasar vets."),
            ("Local cafés &amp; warungs", "Genius Cafe, Manik Organik, Cafe Locca — dog-tolerant outdoor seating."),
        ],
        "delivery": "Bike pickup &amp; drop-off throughout Sanur, Mertasari, Semawang and the Renon border (extra IDR 450,000–750,000 depending on location).",
        "neighbours": ["denpasar", "ubud", "uluwatu"],
    },
]

AREA_BY_SLUG = {a["slug"]: a for a in AREAS}

WA_BASE = "https://wa.me/6281808029595"

def wa(msg):
    from urllib.parse import quote
    return f"{WA_BASE}?text={quote(msg)}"

def render(a):
    name = a["name"]; slug = a["slug"]
    title = f"Dog Pods {name} Bali — Custom Fibreglass Dog Carriers Fitted in {name} | Dharma's Dog Pods"
    desc = (f"Custom dog pods fitted in {name}, Bali. Hand-laid fibreglass dog carriers built for any "
            f"moped or scooter — Vario, NMAX, Scoopy, PCX, Vespa. From IDR 2,400,000, ready in 4–7 days. "
            f"WhatsApp Dharma on +62 818 0802 9595.")
    canonical = f"https://dogpodsbali.com/dog-pods-{slug}.html"

    spots_html = "\n".join(
        f'        <article class="bg-white rounded-2xl p-5 border border-black/5 shadow-sm">\n'
        f'          <h3 class="font-[Fraunces] font-bold text-lg">{title_}</h3>\n'
        f'          <p class="mt-1 text-sm text-[var(--ink)]/75">{desc_}</p>\n'
        f'        </article>'
        for title_, desc_ in a["spots"]
    )

    neighbour_links = "\n".join(
        f'        <a href="/dog-pods-{n}.html" class="bg-white rounded-xl px-4 py-3 border border-black/5 font-medium hover:border-[var(--terracotta)]">Dog Pods {AREA_BY_SLUG[n]["name"]}</a>'
        for n in a["neighbours"]
    )

    wa_quote = wa(f"Hi Dharma, I'm in {name} and I'd like a quote for a dog pod. My bike model: \nMy dog's size: \nSingle or double side: \nAnything else: ")
    wa_general = wa(f"Hi Dharma, I'd like to ask about a dog pod for my bike in {name}, Bali")
    wa_book = wa(f"Hi Dharma, I'd like to book a build slot for a dog pod, fitted in {name}")

    faq_questions = [
        (
            f"Can I get a dog pod fitted in {name}, Bali?",
            f"Yes — Dharma fits dog pods all over Bali, including throughout {name}. Most builds are completed in 4–7 days average and fitted to your bike at a location convenient for you in {name}."
        ),
        (
            f"How much does a dog pod cost in {name}?",
            "Single-side pods start from IDR 2,400,000 and double-side pods start from IDR 3,400,000. Final price depends on your bike model and the size of pod your dog needs. Tell Dharma your bike model and request on WhatsApp for an exact quote."
        ),
        (
            f"How long does it take to make and fit a dog pod in {name}?",
            f"Typically 4–7 days average from the time you confirm the build. Once it's ready, Dharma will arrange a fitting time in {name}."
        ),
        (
            f"Will the pod fit my scooter — Honda Vario, Yamaha NMAX, Vespa, etc?",
            "Yes. Every pod is custom-built to your bike's rack — Honda Vario, Scoopy, PCX, BeAT, Genio, ADV, Yamaha NMAX, Aerox, Fazzio, Mio, Vespa LX/Sprint/GTS, Kawasaki, Suzuki, Royal Enfield and more. Send a photo of your bike on WhatsApp."
        ),
        (
            f"Why should I choose a fibreglass dog pod over a wooden one in {name}?",
            f"Bali's tropical climate destroys plywood pods within a season — they swell, warp, grow mould and rot. Dharma's pods are hand-laid fibreglass with a UV-stable gel coat — fully waterproof, mould-proof, lighter and stronger. The same material used for boats and surfboards in Bali, because nothing else holds up here long-term."
        ),
        (
            f"Do you deliver and fit dog pods in {name}?",
            f"Yes — {a['delivery']} For other parts of Bali we'll arrange a fitting time that works for both of us."
        ),
        (
            f"Can you pick up my bike and drop it back to me in {name}?",
            f"Yes. We can collect your moped or scooter from your villa, fit the pod at the workshop, and drop it back ready to ride. The pickup-and-drop-off service is an extra IDR 450,000–750,000 depending on where you are in {name} — Dharma will confirm the exact figure on WhatsApp once he knows your location."
        ),
    ]

    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": ans}}
            for q, ans in faq_questions
        ]
    }

    breadcrumb_jsonld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://dogpodsbali.com/"},
            {"@type": "ListItem", "position": 2, "name": f"Dog Pods {name}", "item": canonical},
        ]
    }

    localbiz_jsonld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": f"Dharma's Dog Pods — {name}",
        "url": canonical,
        "telephone": "+62 818 0802 9595",
        "priceRange": "IDR 2,400,000 – IDR 3,400,000+",
        "image": "https://dogpodsbali.com/blacknmaxdogpodbali.png",
        "areaServed": {"@type": "Place", "name": f"{name}, Bali, Indonesia"},
        "address": {"@type": "PostalAddress", "addressLocality": name, "addressRegion": "Bali", "addressCountry": "ID"},
        "description": f"Custom hand-laid fibreglass dog pods built and fitted in {name}, Bali. For any moped, scooter or motorbike. From IDR 2,400,000.",
    }

    faq_html = "\n".join(
        f'        <details class="faq-item bg-white rounded-xl border border-black/5 px-5 py-4">\n'
        f'          <summary class="flex justify-between items-center font-semibold">{q}<span class="chev" aria-hidden="true">▾</span></summary>\n'
        f'          <p class="mt-3 text-[var(--ink)]/80">{ans}</p>\n'
        f'        </details>'
        for q, ans in faq_questions
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{canonical}" />

  <meta property="og:type" content="website" />
  <meta property="og:title" content="Dog Pods {name} Bali — Dharma's Dog Pods" />
  <meta property="og:description" content="Custom fibreglass dog pods fitted in {name}, Bali. For any moped or scooter. From IDR 2,400,000." />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://dogpodsbali.com/blacknmaxdogpodbali.png" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Dog Pods {name} Bali — Dharma's Dog Pods" />
  <meta name="twitter:description" content="Custom fibreglass dog pods fitted in {name}, Bali. From IDR 2,400,000, ready in 4–7 days." />
  <meta name="twitter:image" content="https://dogpodsbali.com/blacknmaxdogpodbali.png" />

  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="theme-color" content="#c8623c" />
  <meta name="geo.region" content="ID-BA" />
  <meta name="geo.placename" content="{name}, Bali, Indonesia" />

  <link rel="icon" type="image/png" href="/dharms-dog-pods-logo.png" />
  <link rel="apple-touch-icon" href="/dharms-dog-pods-logo.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="/styles.css" />

  <script type="application/ld+json">
{json.dumps(breadcrumb_jsonld, indent=2)}
  </script>

  <script type="application/ld+json">
{json.dumps(localbiz_jsonld, indent=2)}
  </script>

  <script type="application/ld+json">
{json.dumps(faq_jsonld, indent=2)}
  </script>
</head>
<body class="bg-[var(--cream)]">

  <header class="sticky top-0 z-40 bg-[var(--cream)]/90 backdrop-blur border-b border-black/5">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
      <span class="md:hidden w-10 h-10" aria-hidden="true"></span>
      <a href="/" class="flex items-center gap-2.5 md:mr-auto" aria-label="Dharma's Dog Pods home">
        <img src="/dharms-dog-pods-logo.png" alt="Dharma's Dog Pods — Bali moped dog pod add-ons" width="72" height="72" class="w-[72px] h-[72px] md:w-14 md:h-14 object-contain" />
        <span class="font-[Fraunces] font-bold text-base md:text-lg leading-tight text-[var(--ink)] hidden md:inline">Dharma's Dog Pods</span>
      </a>
      <button class="nav-toggle md:hidden inline-flex items-center justify-center w-10 h-10 rounded-md border border-black/10" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
      <nav id="primary-nav" class="nav-menu hidden md:flex absolute md:static top-full left-0 right-0 md:top-auto bg-[var(--cream)] md:bg-transparent flex-col md:flex-row gap-1 md:gap-6 px-4 md:px-0 py-4 md:py-0 border-b border-black/5 md:border-0">
        <a href="/" class="px-3 py-2 rounded-md hover:text-[var(--terracotta)] font-medium">Home</a>
        <a href="/custom-dog-pods.html" class="px-3 py-2 rounded-md hover:text-[var(--terracotta)] font-medium">Custom Dog Pods</a>
        <a href="/blog.html" class="px-3 py-2 rounded-md hover:text-[var(--terracotta)] font-medium">Blog</a>
        <a href="/faq.html" class="px-3 py-2 rounded-md hover:text-[var(--terracotta)] font-medium">FAQ</a>
        <a href="/contact.html" class="px-3 py-2 rounded-md hover:text-[var(--terracotta)] font-medium">Contact</a>
        <a href="{wa('Hi Dharma, I would like a quote for a custom dog pod')}" class="btn btn-wa md:ml-2" rel="noopener" target="_blank">WhatsApp Dharma</a>
      </nav>
    </div>
  </header>

  <nav class="max-w-7xl mx-auto px-4 sm:px-6 pt-4 text-sm text-[var(--ink)]/60" aria-label="Breadcrumb">
    <a href="/" class="hover:underline">Home</a> <span aria-hidden="true">›</span> <span class="text-[var(--ink)]/80">Dog Pods {name}</span>
  </nav>

  <!-- HERO -->
  <section class="paw-bg">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 pt-10 sm:pt-16 pb-12 text-center">
      <p class="inline-block bg-[var(--terracotta)]/10 text-[var(--terracotta-dark)] font-semibold text-sm px-3 py-1 rounded-full mb-4">Serving {name}, Bali</p>
      <h1 class="font-[Fraunces] text-4xl sm:text-5xl font-bold leading-[1.05]">Dog Pods in {name}, Bali — Custom-Fitted to Your Bike</h1>
      <p class="mt-4 text-lg text-[var(--ink)]/75 max-w-2xl mx-auto">{a['tagline']}.</p>
      <div class="mt-7 flex flex-col sm:flex-row gap-3 justify-center">
        <a href="{wa_quote}" class="btn btn-wa" rel="noopener" target="_blank">Get a quote for {name}</a>
        <a href="/custom-dog-pods.html" class="btn btn-outline">See pod options</a>
      </div>
      <ul class="mt-8 grid grid-cols-3 gap-4 text-sm max-w-md mx-auto">
        <li class="flex flex-col items-center"><span class="font-bold text-[var(--terracotta)] text-2xl">4–7</span><span class="text-[var(--ink)]/70">days avg build</span></li>
        <li class="flex flex-col items-center"><span class="font-bold text-[var(--terracotta)] text-2xl">2.4M</span><span class="text-[var(--ink)]/70">IDR from</span></li>
        <li class="flex flex-col items-center"><span class="font-bold text-[var(--terracotta)] text-2xl">100%</span><span class="text-[var(--ink)]/70">fitted in {name}</span></li>
      </ul>
    </div>
  </section>

  <!-- INTRO -->
  <section class="bg-[var(--cream)]">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
      <h2 class="font-[Fraunces] text-3xl font-bold">Where can I get a dog pod in {name}?</h2>
      <p class="mt-4 text-lg text-[var(--ink)]/85 leading-relaxed">{a['intro']}</p>
      <p class="mt-3 text-lg text-[var(--ink)]/85 leading-relaxed">Dharma builds every pod by hand from <a href="/custom-dog-pods.html#fibreglass" class="text-[var(--terracotta)] underline">marine-grade fibreglass</a>, sized around your dog and fitted directly to your bike's rack. {a['delivery']}</p>
    </div>
  </section>

  <!-- LOCAL SPOTS -->
  <section class="bg-[var(--sand)]">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-14">
      <h2 class="font-[Fraunces] text-3xl font-bold text-center">Where you'll be riding in {name} with your dog</h2>
      <p class="text-center mt-3 text-[var(--ink)]/75 max-w-xl mx-auto">A pod opens up the parts of {name} you'd otherwise leave the dog at home for.</p>
      <div class="mt-8 grid sm:grid-cols-2 gap-5">
{spots_html}
      </div>
    </div>
  </section>

  <!-- PRICING REMINDER -->
  <section class="bg-[var(--cream)]">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-14">
      <div class="grid md:grid-cols-2 gap-6">
        <article class="bg-white rounded-3xl shadow-xl border border-black/5 p-7 flex flex-col">
          <p class="font-semibold text-[var(--terracotta)] uppercase tracking-wide text-xs">Single-Side Pod</p>
          <p class="mt-2 font-[Fraunces] text-3xl sm:text-4xl font-bold">From IDR 2,400,000</p>
          <p class="mt-2 text-[var(--ink)]/70 text-sm">One pod, one side. Best for smaller bikes and small-to-medium dogs.</p>
        </article>
        <article class="bg-white rounded-3xl shadow-xl border-2 border-[var(--terracotta)]/40 p-7 flex flex-col relative">
          <span class="absolute -top-3 right-6 bg-[var(--terracotta)] text-white text-xs font-semibold uppercase tracking-wide px-3 py-1 rounded-full">Most popular</span>
          <p class="font-semibold text-[var(--terracotta)] uppercase tracking-wide text-xs">Double-Side Pod</p>
          <p class="mt-2 font-[Fraunces] text-3xl sm:text-4xl font-bold">From IDR 3,400,000</p>
          <p class="mt-2 text-[var(--ink)]/70 text-sm">Twin pods — balanced ride, more room. Best for larger bikes and bigger dogs.</p>
        </article>
      </div>
      <div class="text-center mt-8">
        <a href="{wa_quote}" class="btn btn-wa" rel="noopener" target="_blank">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M20.52 3.48A11.86 11.86 0 0 0 12.06 0C5.5 0 .14 5.36.14 11.92c0 2.1.55 4.16 1.6 5.97L0 24l6.27-1.65a11.9 11.9 0 0 0 5.79 1.48h.01c6.56 0 11.92-5.36 11.92-11.92 0-3.18-1.24-6.17-3.47-8.43z"/></svg>
          Tell Dharma your bike &amp; request — {name}
        </a>
      </div>
    </div>
  </section>

  <!-- BIKE PICKUP & DROP-OFF -->
  <section class="bg-[var(--sand)]">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-12">
      <div class="bg-white rounded-3xl border border-black/5 shadow-md p-7 sm:p-9 grid md:grid-cols-[auto,1fr,auto] gap-6 items-center">
        <div class="text-5xl" aria-hidden="true">🛵</div>
        <div>
          <p class="font-semibold text-[var(--terracotta)] uppercase tracking-wide text-xs">Bike pickup &amp; drop-off · {name}</p>
          <h2 class="font-[Fraunces] text-2xl sm:text-3xl font-bold mt-1">Don't want to ride to the workshop? We'll come to you.</h2>
          <p class="mt-2 text-[var(--ink)]/80">{a['delivery'].replace('Bike pickup &amp; drop-off', 'We pick up your bike, fit the pod, and drop it back to you')} Add it to any single-side or double-side pod build.</p>
          <p class="mt-2 text-sm text-[var(--ink)]/65">Final figure depends on the exact spot in {name} and the time of day. Confirmed on WhatsApp before we start.</p>
        </div>
        <a href="{wa_quote}" class="btn btn-wa whitespace-nowrap" rel="noopener" target="_blank">Get a {name} quote</a>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="bg-[var(--cream)]">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 py-14">
      <h2 class="font-[Fraunces] text-3xl font-bold text-center">Dog pods in {name} — FAQ</h2>
      <p class="text-center mt-3 text-[var(--ink)]/75">Everything {name} dog owners ask before booking.</p>
      <div class="mt-8 space-y-3">
{faq_html}
      </div>
    </div>
  </section>

  <!-- NEIGHBOURS -->
  <section class="bg-[var(--sand)]">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-14 text-center">
      <h2 class="font-[Fraunces] text-2xl font-bold">Also serving nearby</h2>
      <p class="mt-3 text-[var(--ink)]/75">Dharma fits dog pods across the whole island.</p>
      <div class="mt-6 flex flex-wrap justify-center gap-3">
{neighbour_links}
        <a href="/contact.html" class="bg-white rounded-xl px-4 py-3 border border-black/5 font-medium hover:border-[var(--terracotta)]">All other areas →</a>
      </div>
    </div>
  </section>

  <!-- CONTACT -->
  <section class="bg-[var(--terracotta)] text-white">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 py-14 text-center">
      <h2 class="font-[Fraunces] text-3xl font-bold">Ready to ride {name} with your dog?</h2>
      <p class="mt-4 text-white/90 text-lg">Message Dharma directly. Tell him your bike model, your dog's size and what colour you're thinking — quote and build slot the same day.</p>
      <p class="mt-6 font-semibold">Dharma · WhatsApp +62 818 0802 9595</p>
      <a href="{wa_book}" class="btn bg-white text-[var(--terracotta)] hover:bg-[var(--sand)] mt-6" rel="noopener" target="_blank">Book a build slot in {name}</a>
    </div>
  </section>

  <footer class="bg-[var(--ink)] text-white/80">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-12 grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
      <div>
        <div class="flex items-center gap-3"><img src="/dharms-dog-pods-logo.png" alt="Dharma's Dog Pods logo" width="56" height="56" class="w-14 h-14 object-contain bg-white/95 rounded-lg p-1" /><p class="font-[Fraunces] text-xl font-bold text-white">Dharma's Dog Pods</p></div>
        <p class="mt-2 text-sm">Hand-laid fibreglass dog pods, built in Bali. Custom-fitted to your bike, sized around your dog.</p>
      </div>
      <div>
        <p class="font-semibold text-white">Contact</p>
        <ul class="mt-2 text-sm space-y-1">
          <li>Bali, Indonesia</li>
          <li>WhatsApp: <a class="underline" href="https://wa.me/6281808029595" target="_blank" rel="noopener">+62 818 0802 9595</a></li>
          <li>Owner: Dharma</li>
        </ul>
      </div>
      <div>
        <p class="font-semibold text-white">Sitemap</p>
        <ul class="mt-2 text-sm space-y-1">
          <li><a class="hover:underline" href="/">Home</a></li>
          <li><a class="hover:underline" href="/custom-dog-pods.html">Custom Dog Pods</a></li>
          <li><a class="hover:underline" href="/blog.html">Blog</a></li>
          <li><a class="hover:underline" href="/faq.html">FAQ</a></li>
          <li><a class="hover:underline" href="/contact.html">Contact</a></li>
          <li><a class="hover:underline" href="/sitemap.xml">XML sitemap</a></li>
        </ul>
      </div>
      <div>
        <p class="font-semibold text-white">Areas served</p>
        <ul class="mt-2 text-sm space-y-1">
          <li><a class="hover:underline" href="/dog-pods-canggu.html">Dog Pods Canggu</a></li>
          <li><a class="hover:underline" href="/dog-pods-pererenan.html">Dog Pods Pererenan</a></li>
          <li><a class="hover:underline" href="/dog-pods-ubud.html">Dog Pods Ubud</a></li>
          <li><a class="hover:underline" href="/dog-pods-uluwatu.html">Dog Pods Uluwatu</a></li>
          <li><a class="hover:underline" href="/dog-pods-seminyak.html">Dog Pods Seminyak</a></li>
          <li><a class="hover:underline" href="/dog-pods-denpasar.html">Dog Pods Denpasar</a></li>
          <li><a class="hover:underline" href="/dog-pods-sanur.html">Dog Pods Sanur</a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-white/10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 py-4 text-xs flex flex-wrap items-center justify-between gap-2">
        <p>© <span id="year"></span> Dharma's Dog Pods · Bali, Indonesia</p>
        <p>Custom fibreglass dog pods · {name} · Bali</p>
      </div>
    </div>
  </footer>

  <a class="wa-float" href="{wa_general}" target="_blank" rel="noopener" aria-label="Chat with Dharma on WhatsApp">
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.52 3.48A11.86 11.86 0 0 0 12.06 0C5.5 0 .14 5.36.14 11.92c0 2.1.55 4.16 1.6 5.97L0 24l6.27-1.65a11.9 11.9 0 0 0 5.79 1.48h.01c6.56 0 11.92-5.36 11.92-11.92 0-3.18-1.24-6.17-3.47-8.43z"/></svg>
    <span class="hidden sm:inline">Chat with Dharma</span>
  </a>

  <script src="/script.js" defer></script>
</body>
</html>
"""

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for a in AREAS:
        path = f"dog-pods-{a['slug']}.html"
        with open(path, "w") as f:
            f.write(render(a))
        print(f"wrote {path}")
