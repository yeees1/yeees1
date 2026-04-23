import json, os, re, urllib.request

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = "yeees1"

# Маппинг GitHub language -> skillicons key
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
    "Elixir": "elixir", "Clojure": "clojure",
    "Zig": "zig", "Nim": "nim",
}

def api(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    })
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# Собираем языки по всем репозиториям
repos = api(f"https://api.github.com/users/{USERNAME}/repos?per_page=100")
lang_bytes = {}
for repo in repos:
    if repo["name"] == USERNAME:
        continue
    langs = api(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/languages")
    for lang, b in langs.items():
        lang_bytes[lang] = lang_bytes.get(lang, 0) + b

# Сортируем по объёму кода
sorted_langs = sorted(lang_bytes.items(), key=lambda x: -x[1])
known = [(lang, SKILLICONS[lang]) for lang, _ in sorted_langs if lang in SKILLICONS]

print("Detected languages:", [l for l, _ in known])

# Строим HTML-блок с иконками
if known:
    icons_html = '<div align="center">\n'
    parts = []
    for lang, icon in known:
        parts.append(f'  <img src="https://skillicons.dev/icons?i={icon}" height="40" alt="{lang}" />')
    icons_html += '\n  <img width="12" />\n'.join(parts)
    icons_html += '\n</div>'
else:
    icons_html = '<div align="center"></div>'

# Обновляем README между маркерами
with open("README.md", "r") as f:
    content = f.read()

new_content = re.sub(
    r"<!-- LANG_ICONS_START -->.*?<!-- LANG_ICONS_END -->",
    f"<!-- LANG_ICONS_START -->\n{icons_html}\n<!-- LANG_ICONS_END -->",
    content,
    flags=re.DOTALL
)

with open("README.md", "w") as f:
    f.write(new_content)

print("README updated successfully")
