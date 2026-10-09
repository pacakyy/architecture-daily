import streamlit as st
import streamlit.components.v2 as components
import feedparser
import re
import requests
from bs4 import BeautifulSoup
import json
import os
from html import unescape
from datetime import datetime, timedelta

# =========================================================
# APP MEMORY
# =========================================================

DATA_FILE = "app_data.json"


def load_app_data():

    if not os.path.exists(DATA_FILE):

        return {
            "last_visit": None,
            "saved": []
        }

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return {
            "last_visit": None,
            "saved": []
        }


def save_app_data(data):

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )


# ---------------------------------------------------------
# LOAD ONCE PER SESSION
# ---------------------------------------------------------

if "app_data" not in st.session_state:

    st.session_state.app_data = load_app_data()

    st.session_state.previous_visit = (
        st.session_state.app_data["last_visit"]
    )

    st.session_state.app_data["last_visit"] = (
        datetime.now().astimezone().isoformat()
    )

    save_app_data(
        st.session_state.app_data
    )

# =========================================================
# USTAWIENIA
# =========================================================

st.set_page_config(
    page_title="Architecture Daily",
    page_icon="⌂",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

    .stApp {
        background-color: #F7F6F2;
        color: #222222;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 3.5rem;
        padding-bottom: 6rem;
        padding-left: 4rem;
        padding-right: 4rem;
    }

.site-title {
    font-family: Georgia, serif;
    font-size: 3.4rem;
    line-height: 1;
    font-weight: 400;
    letter-spacing: -0.04em;
    color: #202020;
    margin-bottom: 0.35rem;
}

.site-subtitle {
    font-family: Arial, sans-serif;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    color: #817D76;
    margin-bottom: 2.5rem;
}

.site-date {
    font-family: Arial, sans-serif;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #817D76;
    border-bottom: 1px solid #D8D5CE;
    padding-bottom: 0.8rem;
    margin-bottom: 3rem;
}

    /* HEADER */

    .main-title {
        font-family: Georgia, serif;
        font-size: 3.4rem;
        font-weight: 400;
        letter-spacing: -0.055em;
        color: #1E1E1E;
        line-height: 1;
    }

    .main-subtitle {
        font-family: Arial, sans-serif;
        font-size: 0.72rem;
        color: #77736D;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-top: 0.7rem;
    }

    .date-line {
        font-family: Arial, sans-serif;
        font-size: 0.72rem;
        color: #99958E;
        letter-spacing: 0.05em;
        margin-top: 0.35rem;
    }

    .separator {
        height: 1px;
        background-color: #D8D5CE;
        margin-top: 2.5rem;
        margin-bottom: 0.1rem;
    }


   /* =========================================================
   ARTICLE CARDS
   ========================================================= */

.card-meta {
    font-family: Arial, sans-serif;
    font-size: 0.66rem;
    line-height: 1.3;
    text-transform: uppercase;
    letter-spacing: 0.11em;
    color: #817D76;

    margin-top: 0.9rem;
    margin-bottom: 0.5rem;
}


.card-title {
    font-family: Georgia, serif;
    font-size: 1.25rem;
    line-height: 1.12;
    font-weight: 400;
    letter-spacing: -0.025em;

    color: #202020;

    margin-bottom: 0.55rem;
}


.author {
    font-family: Arial, sans-serif;
    font-size: 0.68rem;
    line-height: 1.3;
    text-transform: uppercase;
    letter-spacing: 0.1em;

    color: #8A867F;

    margin-bottom: 0.8rem;
}


.card-description {
    font-family: Arial, sans-serif;
    font-size: 0.78rem;
    line-height: 1.55;

    color: #65615B;

    margin-bottom: 0.75rem;
}


.source-link {
    font-family: Arial, sans-serif;
    font-size: 0.68rem;
    line-height: 1.3;
    text-transform: uppercase;
    letter-spacing: 0.1em;

    color: #45423E;

    text-decoration: none;
}


.source-link:hover {
    color: #000000;
}


    /* IMAGES */

    .article-image {
    transition: transform 0.3s ease;
}

.article-image:hover {
    transform: scale(1.015);
}


    /* STREAMLIT */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background-color: transparent !important;
    }

    div[data-testid="column"] {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    /* =========================================================
   FEED LAYOUT
   ========================================================= */

[data-testid="stHorizontalBlock"] {
    align-items: flex-start;
}

[data-testid="column"] {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
}


/* =========================================================
   ARTICLE IMAGE
   ========================================================= */

[data-testid="stImage"] img {
    width: 100%;
    display: block;
}


/* =========================================================
   ARTICLE SPACING
   ========================================================= */

.card-meta {
    margin-top: 1rem;
}

.card-title {
    margin-bottom: 0.7rem;
}

.card-description {
    max-width: 42rem;
}


/* =========================================================
   ARTICLE HOVER
   ========================================================= */

[data-testid="stImage"] img {
    transition: opacity 0.25s ease;
}

[data-testid="stImage"]:hover img {
    opacity: 0.88;
}

/* =========================================================
   SOURCE FILTER
   ========================================================= */

div[role="radiogroup"] {
    gap: 1.5rem;
    margin-bottom: 2.5rem;
}

div[role="radiogroup"] label {
    font-family: Arial, sans-serif;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.11em;
    color: #45423E !important;
}

/* =========================================================
   FILTER BAR
   ========================================================= */

.filter-bar {
    margin-top: 0;
    margin-bottom: 2.5rem;
}

.stButton > button {
    background-color: transparent !important;
    color: #817D76 !important;

    border: none !important;
    border-radius: 0 !important;

    font-family: Arial, sans-serif !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.11em !important;

    padding: 0.2rem 0 !important;
    min-height: 0 !important;

    box-shadow: none !important;
    
    text-align: left !important;
}

.stButton > button:hover {
    background-color: transparent !important;
    color: #202020 !important;
    border: none !important;
}

/* FILTER BAR SPACING */

.filter-bar + div {
    margin-bottom: 0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNKCJE
# =========================================================

def clean_html(text):
    text = re.sub("<[^<]+?>", "", text)
    return unescape(text).strip()


def parse_date(article):

    published = article.get(
        "published",
        ""
    )

    if not published:

        return datetime.min

    try:

        # Divisare — ISO 8601
        # np. 2026-10-08T14:05:42Z

        if "T" in published and "-" in published:

            date = datetime.fromisoformat(
                published.replace(
                    "Z",
                    "+00:00"
                )
            )

            return date.astimezone().replace(
                tzinfo=None
            )


        # ArchDaily / pozostałe RSS
        # np. Thu, 08 Oct 2026 13:00:00 +0000

        date = datetime(
            int(published[12:16]),

            datetime.strptime(
                published[8:11],
                "%b"
            ).month,

            int(published[5:7]),

            int(published[17:19]),
            int(published[20:22]),
            int(published[23:25])
        )

        # ArchDaily podaje UTC
        return date + timedelta(hours=2)


    except:

        return datetime.min

def format_date(date):

    if date == datetime.min:
        return ""

    today = datetime.now().date()
    article_date = date.date()

    if article_date == today:
        label = "TODAY"

    elif article_date == today - timedelta(days=1):
        label = "YESTERDAY"

    else:
        label = date.strftime("%d.%m.%Y")

    return f"{label} · {date.strftime('%H:%M')}"


def get_image(article):

    # Najpierw sprawdzamy standardowe enclosure
    for link in article.get("links", []):

        if link.get("rel") == "enclosure":

            return link.get("href")


    # Divisare umieszcza obraz w HTML-u content
    content = article.get("content", [])

    if content:

        html = content[0].get("value", "")

        match = re.search(
            r'<img[^>]+src=["\']([^"\']+)["\']',
            html
        )

        if match:

            return match.group(1)


    return None


# =========================================================
# POBIERANIE ŹRÓDEŁ
# =========================================================

@st.cache_data(ttl=600)
def get_murator_articles():

    url = "https://architektura.muratorplus.pl/architektura/"

    response = requests.get(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    cards = soup.find_all(
        "div",
        class_="element type--article"
    )

    articles = []

    seen_links = set()

    for card in cards:

        link_element = card.select_one(
            ".element__headline a"
        )

        image_element = card.select_one(
            ".element__media img:not(.lead-gallery-more img)"
        )

        if not link_element:

            continue

        link = link_element.get(
            "href"
        )

        if not link or link in seen_links:

            continue

        seen_links.add(link)

        title = link_element.get_text(
            " ",
            strip=True
        )

        image = (
            image_element.get("src")
            if image_element
            else None
        )

        try:

            article_response = requests.get(
                link,
                timeout=10
            )

            article_soup = BeautifulSoup(
                article_response.text,
                "html.parser"
            )

            data = None

            for script in article_soup.find_all(
                "script",
                type="application/ld+json"
            ):

                try:

                    candidate = json.loads(
                        script.string
                    )

                    if (
                        isinstance(candidate, dict)
                        and "datePublished" in candidate
                    ):

                        data = candidate
                        break

                except:

                    continue

            if not data:

                continue

            author = data.get(
                "author",
                []
            )

            if author:

                author = author[0].get(
                    "name",
                    ""
                )

            else:

                author = ""

            articles.append({

                "source": "Architektura-Murator",

                "title": title,

                "author": author,

                "date": datetime.fromisoformat(
                    data["datePublished"]
                ).astimezone().replace(
                    tzinfo=None
                ),

                "image": image,

                "summary": data.get(
                    "description",
                    ""
                ),

                "link": link

            })

        except:

            continue

    return articles

ARCHDAILY_RSS = "https://www.archdaily.com/rss.xml"
DEZEEN_RSS = "https://www.dezeen.com/architecture/feed/"
DESIGNBOOM_RSS = "https://www.designboom.com/architecture/feed/"
DIVISARE_RSS = "https://divisare.com/publications/11/feed"

archdaily_feed = feedparser.parse(ARCHDAILY_RSS)
dezeen_feed = feedparser.parse(DEZEEN_RSS)
designboom_feed = feedparser.parse(DESIGNBOOM_RSS)
divisare_feed = feedparser.parse(DIVISARE_RSS)

# =========================================================
# NORMALIZACJA DANYCH
# =========================================================

def add_articles(feed, source):

    for article in feed.entries:

        publication_date = parse_date(article)

                # Divisare może zwracać ten sam projekt kilka razy
        if source == "Divisare":

            title = article.get(
                "title",
                ""
            )

            if any(
                existing["source"] == "Divisare"
                and existing["title"] == title
                for existing in articles
            ):

                continue

        articles.append({

            "source": source,

            "title": article.get(
                "title",
                "Bez tytułu"
            ),

            "author": article.get(
                "author",
                ""
            ),

            "date": publication_date,

            "image": get_image(article),

            "summary": (
                ""
                if source == "Divisare"
                else clean_html(
                    article.get("summary", "")
                )
            ),

            "link": article.get(
                "link",
                "#"
            )

        })


articles = []


# =========================================================
# DODAWANIE ŹRÓDEŁ
# =========================================================

add_articles(
    archdaily_feed,
    "ArchDaily"
)

add_articles(
    dezeen_feed,
    "Dezeen"
)

add_articles(
    designboom_feed,
    "designboom"
)

add_articles(
    divisare_feed,
    "Divisare"
)

murator_articles = get_murator_articles()

articles.extend(
    murator_articles
)

# =========================================================
# SORTOWANIE
# =========================================================

articles.sort(
    key=lambda article: article["date"],
    reverse=True
)


# =========================================================
# NAGŁÓWEK
# =========================================================

st.markdown(
    '<div class="main-title">Architecture Daily</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'A personal journal of architecture'
    '</div>',
    unsafe_allow_html=True
)

today = datetime.now().strftime("%d.%m.%Y")

st.markdown(
    f'<div class="date-line">{today}</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="separator"></div>',
    unsafe_allow_html=True
)


# =========================================================
# FEED
# =========================================================

# =========================================================
# PAGINATION
# =========================================================

if "articles_to_show" not in st.session_state:

    st.session_state.articles_to_show = 12

# =========================================================
# FILTERS
# =========================================================

sources = [
    "ALL",
    "ArchDaily",
    "Dezeen",
    "designboom",
    "Divisare",
    "Architektura-Murator"
]

views = [
    "ALL",
    "NEW",
    "SAVED"
]


if "selected_source" not in st.session_state:

    st.session_state.selected_source = "ALL"


if "selected_view" not in st.session_state:

    st.session_state.selected_view = "ALL"


selected_source = st.session_state.selected_source

selected_view = st.session_state.selected_view


filter_container = st.container(
    key="sticky_filters"
)

with filter_container:

    left_filter, spacer, right_filter = st.columns(
        [0.9, 2.5, 2.8]
    )


    # LEFT — VIEW FILTERS

    with left_filter:

        view_columns = st.columns(
            [0.7, 0.7, 0.9]
        )

        for index, view in enumerate(views):

            with view_columns[index]:

                if st.button(
                    view,
                    key=f"view_{view}"
                ):

                    st.session_state.selected_view = view

                    st.rerun()


    # RIGHT — SOURCE FILTERS

    with right_filter:

        source_columns = st.columns(
            [
                0.9,
                1.7,
                1.3,
                1.7,
                1.3,
                1.2
            ]
        )

        for index, source in enumerate(sources):

            with source_columns[index]:

                button_label = (
                    "Murator"
                    if source == "Architektura-Murator"
                    else source
                )

                if st.button(
                    button_label,
                    key=f"filter_source_{source}"
                ):

                    st.session_state.selected_source = source

                    st.rerun()


# =========================================================
# RESET PAGINATION WHEN FILTER CHANGES
# =========================================================

if "last_source" not in st.session_state:

    st.session_state.last_source = selected_source
    st.session_state.last_view = selected_view

elif (
    st.session_state.last_source != selected_source
    or st.session_state.last_view != selected_view
):

    st.session_state.articles_to_show = 12

    st.session_state.last_source = selected_source
    st.session_state.last_view = selected_view

# =========================================================
# FILTER ARTICLES
# =========================================================

sticky_component = components.component(
    name="sticky_filters_controller",
    js="""
    export default function() {

        const filter = document.querySelector(
            ".st-key-sticky_filters"
        );

        if (!filter) {
            return;
        }

        const placeholder =
            document.createElement("div");

        placeholder.style.display = "none";

        filter.parentNode.insertBefore(
            placeholder,
            filter
        );


        function stick() {

            if (filter.dataset.isFixed === "true") {
                return;
            }

            const rect =
                filter.getBoundingClientRect();

            placeholder.style.display = "block";
            placeholder.style.width =
                rect.width + "px";
            placeholder.style.height = "48px";
            
            filter.style.minHeight = "48px";
            filter.style.display = "flex";
            filter.style.alignItems = "center";
            filter.style.justifyContent = "center";

            filter.dataset.isFixed = "true";

            filter.style.position = "fixed";
            filter.style.top = "0px";
            filter.style.left =
                rect.left + "px";
            filter.style.width =
                rect.width + "px";

            filter.style.zIndex = "1000000";
            filter.style.backgroundColor =
                "#F7F6F2";
            filter.style.pointerEvents = "auto"; 
            filter.style.boxSizing =
                "border-box";
        }


        function unstick() {

            if (filter.dataset.isFixed !== "true") {
                return;
            }

            filter.dataset.isFixed = "false";

            filter.style.position = "";
            filter.style.top = "";
            filter.style.left = "";
            filter.style.width = "";
            filter.style.zIndex = "";
            filter.style.backgroundColor = "";
            filter.style.boxSizing = "";
            
            filter.style.minHeight = "";
            filter.style.display = "";
            filter.style.alignItems = "";

            placeholder.style.display = "none";
        }


        function handleScroll(event) {

            const filterRect =
                filter.getBoundingClientRect();

            const placeholderRect =
                placeholder.getBoundingClientRect();


            // Filtry są jeszcze normalnie na stronie.
            // Kiedy dojadą do góry — przyklejamy.

            if (
                filter.dataset.isFixed !== "true"
                &&
                filterRect.top <= 0
            ) {

                stick();
                return;
            }


            // Filtry są przyklejone.
            // Kiedy ich normalne miejsce wróci
            // poniżej górnej krawędzi — odklejamy.

            if (
                filter.dataset.isFixed === "true"
                &&
                placeholderRect.top > 0
            ) {

                unstick();
            }
        }


        document.addEventListener(
            "scroll",
            handleScroll,
            true
        );
    }
    """
)

sticky_component()

filtered_articles = articles


# ---------------------------------------------------------
# SOURCE
# ---------------------------------------------------------

if selected_source != "ALL":

    filtered_articles = [
        article
        for article in filtered_articles
        if article["source"] == selected_source
    ]


# ---------------------------------------------------------
# NEW
# ---------------------------------------------------------

if selected_view == "NEW":

    previous_visit = st.session_state.previous_visit

    if previous_visit:

        previous_visit_dt = datetime.fromisoformat(
            previous_visit
        )

        filtered_articles = [
            article
            for article in filtered_articles
            if article["date"] != datetime.min
            and article["date"] > previous_visit_dt
        ]

if selected_view == "SAVED":

    saved_articles = st.session_state.app_data["saved"]

    filtered_articles = [
        article
        for article in filtered_articles
        if article["link"] in saved_articles
    ]

if not articles:

    st.error("Nie znaleziono żadnych artykułów.")

else:

    columns = st.columns(3, gap="medium")


    for index, article in enumerate(filtered_articles[:st.session_state.articles_to_show]):

        with columns[index % 3]:

            # -----------------------------------------
            # ZDJĘCIE
            # -----------------------------------------

            if article["image"]:

                st.markdown(
        f'''
        <a href="{article["link"]}" target="_blank">
            <img
                class="article-image"
                src="{article["image"]}"
            >
        </a>
        ''',
        unsafe_allow_html=True
    )
                


            # -----------------------------------------
            # ŹRÓDŁO + DATA
            # -----------------------------------------

            metadata = article["source"]

            formatted_date = format_date(
                article["date"]
            )

            if formatted_date:

                metadata += (
                    f"  ·  {formatted_date}"
                )

            st.markdown(
                f'<div class="card-meta">'
                f'{metadata}'
                f'</div>',
                unsafe_allow_html=True
            )


            # -----------------------------------------
            # TYTUŁ
            # -----------------------------------------

            st.markdown(
                f'<div class="card-title">'
                f'{article["title"]}'
                f'</div>',
                unsafe_allow_html=True
            )


            # -----------------------------------------
            # AUTOR
            # -----------------------------------------

            if article["author"]:

                st.markdown(
                    f'<div class="author">'
                    f'✦ {article["author"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )


            # -----------------------------------------
            # OPIS
            # -----------------------------------------

            if article["summary"]:

                short_summary = article["summary"][:280]

                if len(article["summary"]) > 280:
                    short_summary += "…"

                st.markdown(
                    f'<div class="card-description">'
                    f'{short_summary}'
                    f'</div>',
                    unsafe_allow_html=True
                )


            # -----------------------------------------
            # LINK
            # -----------------------------------------

            st.markdown(
                f'<a class="source-link" '
                f'href="{article["link"]}" '
                f'target="_blank">'
                f'Open article →'
                f'</a>',
                unsafe_allow_html=True
            )

            # -----------------------------------------
            # SAVE
            # -----------------------------------------

            is_saved = article["link"] in st.session_state.app_data["saved"]

            button_label = "SAVED ✓" if is_saved else "SAVE"

            if st.button(
                button_label,
                key=f"save_{index}_{article['link']}"
            ):

                if is_saved:

                    st.session_state.app_data["saved"].remove(
                        article["link"]
                    )

                else:

                    st.session_state.app_data["saved"].append(
                        article["link"]
                    )

                save_app_data(
                    st.session_state.app_data
                )

                st.rerun()

            st.markdown(
                '<div style="height: 3.5rem;"></div>',
                unsafe_allow_html=True
            )

    # =========================================================
    # LOAD MORE
    # =========================================================

    if len(filtered_articles) > st.session_state.articles_to_show:

        if st.button("LOAD MORE"):

            st.session_state.articles_to_show += 12

            st.rerun()
