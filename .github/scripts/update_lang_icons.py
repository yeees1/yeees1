import json, os, re, urllib.request
from datetime import datetime

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = "yeees1"

SKILLICONS = {
    "Python": "py", "JavaScript": "js", "TypeScript": "ts",
    "C++": "cpp", "C": "c", "C#": "cs", "Go": "go",
    "Rust": "rust", "Java": "java", "Kotlin": "kotlin",
    "Swift": "swift", "Ruby": "ruby", "PHP": "php",
    "Scala": "scala", "Dart": "dart", "R": "r",
    "Shell": "bash", "PowerShell": "powershell",
    "HTML": "html", "CSS": "css", "SCSS": "sass",
    "Vue": "vue", "Svelte": "svelte",
    "Lua": "lua", "Perl": "perl", "Haskell": "haskell",
    "Elixir": "elixir", "Zig": "zig",
}

def api(url):
    req = urllib.request.Request(url, headers={
        "Authorization": "token " + TOKEN,
        "Accept": "application/vnd.github.v3+json"
    })
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# Языки по всем репозиториям
repos = api("https://api.github.com/users/" + USERNAME + "/repos?per_page=100")
lang_bytes = {}
for repo in repos:
    if repo["name"] == USERNAME:
        continue
    name = repo["name"]
    langs = api("https://api.github.com/repos/" + USERNAME + "/" + name + "/languages")
    for lang, b in langs.items():
        lang_bytes[lang] = lang_bytes.get(lang, 0) + b

sorted_langs = sorted(lang_bytes.items(), key=lambda x: -x[1])
known = [(lang, SKILLICONS[lang]) for lang, _ in sorted_langs if lang in SKILLICONS]
print("Detected languages:", [l for l, _ in known])

# HTML-блок с иконками
parts = []
for lang, icon in known:
    parts.append('  <img src="https://skillicons.dev/icons?i=' + icon + '" height="40" alt="' + lang + '" />')
icons_html = '<div align="center">\n' + '\n  <img width="12" />\n'.join(parts) + '\n</div>'

# Читаем README
with open("README.md", "r") as f:
    content = f.read()

# Обновляем иконки языков
content = re.sub(
    r"<!-- LANG_ICONS_START -->.*?<!-- LANG_ICONS_END -->",
    "<!-- LANG_ICONS_START -->\n" + icons_html + "\n<!-- LANG_ICONS_END -->",
    content,
    flags=re.DOTALL
)

# Сбиваем кеш карточек
ts = int(datetime.utcnow().timestamp())

def add_ts(match):
    url = re.sub(r"&t=\d+", "", match.group(1))
    return 'src="' + url + "&t=" + str(ts) + '"'

content = re.sub(
    r'src="(https://github-profile-summary-cards\.vercel\.app/api/cards/[^"]+?)"',
    add_ts,
    content
)

with open("README.md", "w") as f:
    f.write(content)

print("README updated with timestamp " + str(ts))
